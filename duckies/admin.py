from django.contrib import admin

from .models import AttackInventory, AttackItem, Ducky, InventoryItem, Item


@admin.register(Ducky)
class DuckyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "updated_at")
    search_fields = ("name", "owner__username", "owner__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "set_name", "item_type", "rarity", "is_active", "created_at")
    list_filter = ("category", "set_name", "item_type", "rarity", "is_active")
    search_fields = ("name", "description")
    readonly_fields = ("created_at",)
    list_select_related = True


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("ducky", "item", "equipped", "obtained_at")
    list_filter = ("equipped", "item__item_type", "item__rarity")
    search_fields = ("ducky__name", "item__name", "ducky__owner__username")
    readonly_fields = ("obtained_at",)
    list_select_related = ("ducky", "item")


@admin.register(AttackItem)
class AttackItemAdmin(admin.ModelAdmin):
    list_display = (
        "name", "family", "effect", "language", "price", "cooldown_seconds",
        "is_active",
    )
    list_filter = ("family", "effect", "rarity", "language", "is_active")
    search_fields = ("name", "description", "activation_challenge")


@admin.register(AttackInventory)
class AttackInventoryAdmin(admin.ModelAdmin):
    list_display = ("owner", "attack", "quantity", "updated_at")
    list_filter = ("attack__family", "attack__rarity")
    search_fields = ("owner__username", "attack__name")
    list_select_related = ("owner", "attack")
