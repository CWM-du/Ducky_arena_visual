from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Profile
from duckies.models import AttackInventory, AttackItem, Ducky, InventoryItem, Item
from duckies.services import (
    equip_inventory_item,
    grant_item,
    purchase_attack,
    unequip_inventory_item,
)

User = get_user_model()


class InventoryServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="carlos",
            password="pass12345",
        )
        self.ducky = Ducky.objects.create(owner=self.user, name="Byte")
        self.head_a = Item.objects.create(
            name="Gorra SQL",
            item_type=Item.ItemType.HEAD,
        )
        self.head_b = Item.objects.create(
            name="Sombrero Python",
            item_type=Item.ItemType.HEAD,
            rarity=Item.Rarity.RARE,
        )
        self.eyes = Item.objects.create(
            name="Gafas Hacker",
            item_type=Item.ItemType.EYES,
        )

    def test_grant_item_is_idempotent(self):
        first, created = grant_item(self.ducky, self.head_a)
        second, created_again = grant_item(self.ducky, self.head_a)

        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(self.ducky.inventory.count(), 1)

    def test_inactive_item_cannot_be_granted(self):
        from django.core.exceptions import ValidationError

        self.head_a.is_active = False
        self.head_a.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            grant_item(self.ducky, self.head_a)

    def test_equipping_same_category_replaces_previous(self):
        first = InventoryItem.objects.create(
            ducky=self.ducky, item=self.head_a, equipped=True
        )
        second = InventoryItem.objects.create(
            ducky=self.ducky, item=self.head_b
        )

        equip_inventory_item(second)
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(first.equipped)
        self.assertTrue(second.equipped)
        self.assertEqual(
            self.ducky.inventory.filter(
                equipped=True,
                item__item_type=Item.ItemType.HEAD,
            ).count(),
            1,
        )

    def test_different_categories_can_both_be_equipped(self):
        head = InventoryItem.objects.create(
            ducky=self.ducky, item=self.head_a
        )
        eyes = InventoryItem.objects.create(
            ducky=self.ducky, item=self.eyes
        )
        equip_inventory_item(head)
        equip_inventory_item(eyes)

        self.assertEqual(
            self.ducky.inventory.filter(equipped=True).count(),
            2,
        )

    def test_unequip(self):
        inventory_item = InventoryItem.objects.create(
            ducky=self.ducky, item=self.head_a, equipped=True
        )
        unequip_inventory_item(inventory_item)
        inventory_item.refresh_from_db()
        self.assertFalse(inventory_item.equipped)


class AttackShopServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="luna", password="pass12345")
        self.profile, _ = Profile.objects.get_or_create(
            user=self.user,
            defaults={"ducky_coins": 200},
        )
        self.profile.ducky_coins = 200
        self.profile.save(update_fields=["ducky_coins"])
        self.attack = AttackItem.objects.create(
            name="Syntax Lock",
            description="Bloqueo temporal.",
            family=AttackItem.Family.LOCK,
            effect=AttackItem.Effect.LOCK,
            rarity=AttackItem.Rarity.RARE,
            duration_seconds=8,
            cooldown_seconds=24,
            price=90,
            activation_challenge="Identifica la categoría correcta.",
        )

    def test_purchase_spends_coins_and_adds_a_charge(self):
        owned_attack = purchase_attack(self.user, self.attack)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.ducky_coins, 110)
        self.assertEqual(owned_attack.quantity, 1)
        self.assertEqual(AttackInventory.objects.count(), 1)

    def test_purchase_rejects_an_insufficient_balance(self):
        self.profile.ducky_coins = 0
        self.profile.save(update_fields=["ducky_coins"])

        with self.assertRaises(ValidationError):
            purchase_attack(self.user, self.attack)
        self.assertFalse(AttackInventory.objects.exists())
