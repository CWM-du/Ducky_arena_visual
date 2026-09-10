from django.core.exceptions import ValidationError
from django.db import transaction

from accounts.models import Profile

from .models import AttackInventory, AttackItem, Ducky, InventoryItem, Item


@transaction.atomic
def grant_item(ducky: Ducky, item: Item):
    """
    Grant a catalog Item to a Ducky without duplicating the catalog object.

    Safe for repeated calls: the uniqueness constraint plus get_or_create()
    make the operation idempotent for the MVP inventory model.
    """
    if not item.is_active:
        raise ValidationError("No se puede conceder un objeto inactivo.")

    inventory_item, created = InventoryItem.objects.get_or_create(
        ducky=ducky,
        item=item,
    )
    return inventory_item, created


@transaction.atomic
def equip_inventory_item(inventory_item: InventoryItem):
    """
    Equip one owned InventoryItem and clear any equipped item in its category.
    """
    item_type = inventory_item.item.item_type

    (
        InventoryItem.objects
        .select_for_update()
        .filter(
            ducky=inventory_item.ducky,
            equipped=True,
            item__item_type=item_type,
        )
        .exclude(pk=inventory_item.pk)
        .update(equipped=False)
    )

    inventory_item.equipped = True
    inventory_item.save(update_fields=["equipped"])
    return inventory_item


@transaction.atomic
def unequip_inventory_item(inventory_item: InventoryItem):
    inventory_item.equipped = False
    inventory_item.save(update_fields=["equipped"])
    return inventory_item


@transaction.atomic
def purchase_attack(user, attack: AttackItem) -> AttackInventory:
    """Buy one usable attack charge without allowing a negative coin balance."""
    if not attack.is_active:
        raise ValidationError("Este ataque no está disponible en la tienda.")

    profile, _ = Profile.objects.select_for_update().get_or_create(user=user)
    if profile.ducky_coins < attack.price:
        raise ValidationError("No tienes suficientes Ducky Coins.")

    profile.ducky_coins -= attack.price
    profile.save(update_fields=["ducky_coins"])
    owned_attack, _ = AttackInventory.objects.select_for_update().get_or_create(
        owner=user,
        attack=attack,
        defaults={"quantity": 0},
    )
    owned_attack.quantity += 1
    owned_attack.save(update_fields=["quantity", "updated_at"])
    return owned_attack
