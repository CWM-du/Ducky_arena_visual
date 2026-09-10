from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomizationForm, DuckyNameForm
from .models import Ducky, InventoryItem, Item
from .services import equip_inventory_item, unequip_inventory_item


@login_required
def my_ducky(request):
    ducky, _ = Ducky.objects.get_or_create(owner=request.user)
    equipped = (
        ducky.inventory
        .select_related("item")
        .filter(equipped=True)
        .order_by("item__item_type", "item__name")
    )
    equipped_by_type = {
        inventory_item.item.item_type: inventory_item
        for inventory_item in equipped
    }
    return render(
        request,
        "duckies/my_ducky.html",
        {
            "ducky": ducky,
            "equipped_items": equipped,
            "equipped_by_type": equipped_by_type,
            "item_types": Item.ItemType.choices,
        },
    )


@login_required
def rename_ducky(request):
    ducky, _ = Ducky.objects.get_or_create(owner=request.user)

    if request.method == "POST":
        form = DuckyNameForm(request.POST, instance=ducky)
        if form.is_valid():
            form.save()
            messages.success(request, "Has cambiado el nombre de tu Ducky.")
            return redirect("duckies:my_ducky")
    else:
        form = DuckyNameForm(instance=ducky)

    return render(
        request,
        "duckies/ducky_rename.html",
        {"ducky": ducky, "form": form},
    )


@login_required
def inventory(request):
    ducky, _ = Ducky.objects.get_or_create(owner=request.user)
    inventory_items = ducky.inventory.select_related("item").all()

    item_type = request.GET.get("type", "").upper()
    valid_types = {value for value, _ in Item.ItemType.choices}
    if item_type in valid_types:
        inventory_items = inventory_items.filter(item__item_type=item_type)
    else:
        item_type = ""

    return render(
        request,
        "duckies/inventory.html",
        {
            "ducky": ducky,
            "inventory": inventory_items,
            "active_type": item_type,
            "item_types": Item.ItemType.choices,
        },
    )


@login_required
def customize(request):
    ducky, _ = Ducky.objects.get_or_create(owner=request.user)

    if request.method == "POST":
        form = CustomizationForm(request.POST, ducky=ducky)
        if form.is_valid():
            with transaction.atomic():
                selected_ids = {
                    value
                    for value in form.cleaned_data.values()
                    if value
                }
                owned_items = list(
                    ducky.inventory.select_related("item").filter(
                        pk__in=selected_ids
                    )
                )
                selected_by_type = {
                    inventory_item.item.item_type: inventory_item
                    for inventory_item in owned_items
                }

                ducky.inventory.update(equipped=False)
                for inventory_item in selected_by_type.values():
                    inventory_item.equipped = True
                    inventory_item.save(update_fields=["equipped"])

            messages.success(request, "Tu Ducky ha sido personalizado.")
            return redirect("duckies:my_ducky")
    else:
        initial = {
            item_type.lower(): str(inventory_item.pk)
            for inventory_item in (
                ducky.inventory
                .select_related("item")
                .filter(equipped=True)
            )
            for item_type in [inventory_item.item.item_type]
        }
        form = CustomizationForm(
            ducky=ducky,
            initial=initial,
        )

    return render(
        request,
        "duckies/customize.html",
        {"ducky": ducky, "form": form},
    )


@login_required
def equip_item(request, pk):
    if request.method != "POST":
        return redirect("duckies:inventory")

    inventory_item = get_object_or_404(
        InventoryItem.objects.select_related("item", "ducky"),
        pk=pk,
        ducky__owner=request.user,
    )

    if not inventory_item.item.is_active:
        messages.error(request, "Ese objeto ya no está disponible.")
        return redirect("duckies:inventory")

    equip_inventory_item(inventory_item)
    messages.success(
        request,
        f"{inventory_item.item.name} equipado.",
    )
    return redirect("duckies:my_ducky")


@login_required
def unequip_item(request, pk):
    if request.method != "POST":
        return redirect("duckies:inventory")

    inventory_item = get_object_or_404(
        InventoryItem.objects.select_related("item", "ducky"),
        pk=pk,
        ducky__owner=request.user,
    )

    unequip_inventory_item(inventory_item)
    messages.success(
        request,
        f"{inventory_item.item.name} desequipado.",
    )
    return redirect("duckies:my_ducky")
