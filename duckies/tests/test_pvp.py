from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from duckies.models import ActiveEffect, Attack, Ducky, InventoryItem, Item, ItemResistance
from duckies.services import resolve_attack

User = get_user_model()


class PvPAttackTests(TestCase):
    def setUp(self):
        self.attacker = Ducky.objects.create(owner=User.objects.create_user("attacker", password="pass12345"))
        self.defender = Ducky.objects.create(owner=User.objects.create_user("defender", password="pass12345"))
        self.item = Item.objects.create(name="Yelmo de Guardián", item_type=Item.ItemType.HEAD)
        self.inventory = InventoryItem.objects.create(ducky=self.defender, item=self.item, equipped=True)
        self.attack = Attack.objects.create(
            name="Syntax Lock", effect_type=Attack.EffectType.LOCK,
            power=10, duration_seconds=20,
        )

    def test_equipped_item_reduces_attack_power(self):
        ItemResistance.objects.create(item=self.item, effect_type=Attack.EffectType.LOCK, reduction_percent=40)
        result = resolve_attack(self.attacker, self.defender, self.attack)
        self.assertTrue(result["applied"])
        self.assertEqual(result["reduction_percent"], 40)
        self.assertEqual(result["power"], 6)
        self.assertEqual(ActiveEffect.objects.filter(ducky=self.defender).count(), 1)

    def test_full_resistance_prevents_effect(self):
        ItemResistance.objects.create(item=self.item, effect_type=Attack.EffectType.LOCK, reduction_percent=100)
        result = resolve_attack(self.attacker, self.defender, self.attack)
        self.assertFalse(result["applied"])
        self.assertEqual(ActiveEffect.objects.count(), 0)

    def test_multiple_equipped_defenses_stack_with_cap(self):
        body = Item.objects.create(name="Armadura del Dragón Celeste", item_type=Item.ItemType.BODY)
        InventoryItem.objects.create(ducky=self.defender, item=body, equipped=True)
        ItemResistance.objects.create(item=self.item, effect_type=Attack.EffectType.LOCK, reduction_percent=35)
        ItemResistance.objects.create(item=body, effect_type=Attack.EffectType.LOCK, reduction_percent=45)
        result = resolve_attack(self.attacker, self.defender, self.attack)
        self.assertEqual(result["reduction_percent"], 80)
        self.assertEqual(result["power"], 2)

    def test_cannot_attack_self(self):
        with self.assertRaises(ValidationError):
            resolve_attack(self.attacker, self.attacker, self.attack)

    def test_effect_has_expiration(self):
        result = resolve_attack(self.attacker, self.defender, self.attack)
        self.assertGreater(result["effect"].expires_at, timezone.now() + timedelta(seconds=19))
