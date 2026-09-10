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
