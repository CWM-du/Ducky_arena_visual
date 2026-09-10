from django.conf import settings
from django.db import models


class Ducky(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ducky",
    )
    name = models.CharField(max_length=50, default="Ducky")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return f"{self.name} ({self.owner})"


class Item(models.Model):
    class ItemType(models.TextChoices):
        HEAD = "HEAD", "Cabeza"
        EYES = "EYES", "Ojos"
        BODY = "BODY", "Cuerpo"
        ACCESSORY = "ACCESSORY", "Accesorio"

    class Rarity(models.TextChoices):
        COMMON = "COMMON", "Común"
        RARE = "RARE", "Raro"
        EPIC = "EPIC", "Épico"
        LEGENDARY = "LEGENDARY", "Legendario"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    rarity = models.CharField(
        max_length=20,
        choices=Rarity.choices,
        default=Rarity.COMMON,
    )
    image = models.ImageField(
        upload_to="ducky_items/",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]
        indexes = [
            models.Index(fields=["item_type", "is_active"]),
            models.Index(fields=["rarity", "is_active"]),
        ]

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    ducky = models.ForeignKey(
        Ducky,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="owners",
    )
    equipped = models.BooleanField(default=False)
    obtained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-equipped", "-obtained_at", "item__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["ducky", "item"],
                name="unique_item_per_ducky",
            ),
        ]
        indexes = [
            models.Index(fields=["ducky", "equipped"]),
        ]

    def __str__(self):
        return f"{self.ducky.name} - {self.item.name}"
