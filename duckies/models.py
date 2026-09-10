from django.conf import settings
from django.core.validators import MinValueValidator
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


class AttackItem(models.Model):
    """A consumable PvP action sold in the Ducky Shop.

    Attack items deliberately live outside cosmetic ``Item`` objects: equipment
    defines a build, while attacks are spent during a match.
    """

    class Family(models.TextChoices):
        LOCK = "LOCK", "Bloqueo"
        INTERFERENCE = "INTERFERENCE", "Interferencia"
        DELAY = "DELAY", "Retraso"
        SABOTAGE = "SABOTAGE", "Sabotaje"
        CONTROL = "CONTROL", "Control"
        COMBO = "COMBO", "Combo"

    class Effect(models.TextChoices):
        LOCK = "LOCK", "Bloquear acción"
        FREEZE = "FREEZE", "Congelar progreso"
        SILENCE = "SILENCE", "Bloquear habilidad"
        SCRAMBLE = "SCRAMBLE", "Alterar desafío"
        FOG = "FOG", "Ocultar código"
        DELAY = "DELAY", "Retrasar siguiente desafío"
        SLOW = "SLOW", "Reducir progreso"
        PUZZLE = "PUZZLE", "Desafío de escape"
        RESET = "RESET", "Romper combo"
        STACK = "STACK", "Acumular debuff"
        REDIRECT = "REDIRECT", "Cambiar ruta"
        WALL = "WALL", "Bloquear avance"

    class Rarity(models.TextChoices):
        COMMON = "COMMON", "Común"
        RARE = "RARE", "Raro"
        EPIC = "EPIC", "Épico"
        LEGENDARY = "LEGENDARY", "Legendario"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    family = models.CharField(max_length=20, choices=Family.choices)
    effect = models.CharField(max_length=20, choices=Effect.choices)
    rarity = models.CharField(max_length=20, choices=Rarity.choices)
    duration_seconds = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Duración temporal del efecto; vacío si requiere un desafío.",
    )
    cooldown_seconds = models.PositiveSmallIntegerField(default=20)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    activation_challenge = models.CharField(max_length=255)
    language = models.CharField(max_length=30, blank=True, default="")
    required_set = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["family", "price", "name"]
        indexes = [
            models.Index(fields=["family", "is_active"]),
            models.Index(fields=["is_active", "price"]),
        ]

    def __str__(self):
        return self.name


class AttackInventory(models.Model):
    """Charges of an attack owned by a player and purchasable with Ducky Coins."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attack_inventory",
    )
    attack = models.ForeignKey(
        AttackItem,
        on_delete=models.PROTECT,
        related_name="owners",
    )
    quantity = models.PositiveIntegerField(default=0)
    obtained_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "attack"],
                name="unique_attack_per_player",
            ),
        ]
        indexes = [models.Index(fields=["owner", "attack"])]

    def __str__(self):
        return f"{self.owner} - {self.attack} ({self.quantity})"
