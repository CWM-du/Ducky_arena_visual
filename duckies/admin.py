from django.contrib import admin

from .models import ActiveEffect, Attack, Ducky, InventoryItem, Item, ItemResistance


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


@admin.register(Attack)
class AttackAdmin(admin.ModelAdmin):
    list_display = ("name", "effect_type", "language", "power", "duration_seconds", "cooldown_seconds", "difficulty", "is_active")

    list_filter = ("effect_type", "language", "difficulty", "is_active")
    search_fields = ("name", "description", "language")


@admin.register(ItemResistance)
class ItemResistanceAdmin(admin.ModelAdmin):
    list_display = ("item", "effect_type", "reduction_percent", "notes")
    list_filter = ("effect_type", "reduction_percent")
    search_fields = ("item__name", "notes")
    list_select_related = ("item",)


@admin.register(ActiveEffect)
class ActiveEffectAdmin(admin.ModelAdmin):
    list_display = ("ducky", "attack", "effect_type", "power", "expires_at", "created_at")
    list_filter = ("effect_type",)
    search_fields = ("ducky__name", "attack__name")
    readonly_fields = ("created_at",)
    list_select_related = ("ducky", "attack")
