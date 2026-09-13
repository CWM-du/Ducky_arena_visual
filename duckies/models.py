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

    class Category(models.TextChoices):
        STANDARD = "STANDARD", "Estándar"
        ARCANO = "ARCANO", "Arcano"

    class Rarity(models.TextChoices):
        COMMON = "COMMON", "Común"
        RARE = "RARE", "Raro"
        EPIC = "EPIC", "Épico"
        LEGENDARY = "LEGENDARY", "Legendario"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.STANDARD,
    )
    set_name = models.CharField(max_length=100, blank=True, default="")
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
            models.Index(fields=["category", "set_name", "is_active"]),
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

class Attack(models.Model):
    class EffectType(models.TextChoices):
        LOCK = "LOCK", "Bloqueo"
        SLOW = "SLOW", "Lentitud"
        INTERRUPT = "INTERRUPT", "Interrupción"
        SCRAMBLE = "SCRAMBLE", "Código confuso"
        SABOTAGE = "SABOTAGE", "Sabotaje"
        SILENCE = "SILENCE", "Silencio"
        REDIRECT = "REDIRECT", "Redirección"
        RESET = "RESET", "Reinicio"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="ducky_attacks/",
        null=True,
        blank=True,
    )
    effect_type = models.CharField(max_length=20, choices=EffectType.choices)
    power = models.PositiveSmallIntegerField(default=1)
    duration_seconds = models.PositiveIntegerField(default=10)
    cooldown_seconds = models.PositiveIntegerField(default=30)
    language = models.CharField(max_length=50, blank=True, default="")
    difficulty = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "id"]
        indexes = [
            models.Index(fields=["effect_type", "is_active"]),
            models.Index(fields=["language", "is_active"]),
        ]

    def __str__(self):
        return self.name


class ItemResistance(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="resistances",
    )
    effect_type = models.CharField(max_length=20, choices=Attack.EffectType.choices)
    reduction_percent = models.PositiveSmallIntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["item__name", "effect_type"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "effect_type"],
                name="unique_item_resistance_type",
            ),
        ]

    def __str__(self):
        return f"{self.item.name}: {self.effect_type} -{self.reduction_percent}%"


class ActiveEffect(models.Model):
    ducky = models.ForeignKey(
        Ducky,
        on_delete=models.CASCADE,
        related_name="active_effects",
    )
    attack = models.ForeignKey(
        Attack,
        on_delete=models.PROTECT,
        related_name="applied_effects",
    )
    effect_type = models.CharField(max_length=20, choices=Attack.EffectType.choices)
    power = models.PositiveSmallIntegerField(default=1)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["expires_at", "-created_at"]
        indexes = [
            models.Index(fields=["ducky", "effect_type", "expires_at"]),
        ]

    def __str__(self):
        return f"{self.ducky.name}: {self.attack.name}"

