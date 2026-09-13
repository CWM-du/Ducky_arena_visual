from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Ducky, InventoryItem, Item


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

from datetime import timedelta
from django.utils import timezone
from .models import ActiveEffect, Attack


@transaction.atomic
def resolve_attack(attacker: Ducky, defender: Ducky, attack: Attack):
    """Apply a temporary PvP progression debuff after defense mitigation.

    The defender's currently equipped items reduce the attack's power according
    to ItemResistance. No permanent inventory/progression data is removed.
    """
    if attacker.pk == defender.pk:
        raise ValidationError("No puedes atacarte a ti mismo.")
    if not attack.is_active:
        raise ValidationError("Ese ataque no está activo.")

    equipped = (
        defender.inventory
        .select_related("item")
        .filter(equipped=True, item__is_active=True)
    )
    reduction = sum(
        resistance.reduction_percent
        for inventory_item in equipped
        for resistance in inventory_item.item.resistances.all()
        if resistance.effect_type == attack.effect_type
    )
    reduction = min(reduction, 100)
    final_power = max(0, attack.power * (100 - reduction) // 100)

    if final_power == 0:
        return {"applied": False, "power": 0, "reduction_percent": reduction, "effect": None}

    effect = ActiveEffect.objects.create(
        ducky=defender,
        attack=attack,
        effect_type=attack.effect_type,
        power=final_power,
        expires_at=timezone.now() + timedelta(seconds=attack.duration_seconds),
    )
    return {"applied": True, "power": final_power, "reduction_percent": reduction, "effect": effect}
