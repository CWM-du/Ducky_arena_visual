from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

from duckies.models import AttackItem, Ducky, InventoryItem, Item

User = get_user_model()


class DuckyModelTests(TestCase):
    def test_ducky_has_one_owner(self):
        user = User.objects.create_user(username="carlos", password="pass12345")
        ducky = Ducky.objects.create(owner=user, name="Byte")
        self.assertEqual(ducky.owner, user)
        self.assertEqual(user.ducky, ducky)

    def test_ducky_owner_is_unique(self):
        user = User.objects.create_user(username="carlos", password="pass12345")
        Ducky.objects.create(owner=user)
        with self.assertRaises(IntegrityError):
            Ducky.objects.create(owner=user)


class ItemModelTests(TestCase):
    def test_item_choices_and_defaults(self):
        item = Item.objects.create(
            name="Sombrero Python",
            item_type=Item.ItemType.HEAD,
        )
        self.assertEqual(item.item_type, Item.ItemType.HEAD)
        self.assertEqual(item.rarity, Item.Rarity.COMMON)
        self.assertTrue(item.is_active)


class AttackCatalogTests(TestCase):
    def test_seed_catalog_creates_temporary_pvp_attacks(self):
        call_command("seed_catalog", verbosity=0)

        attacks = AttackItem.objects.filter(is_active=True)
        self.assertEqual(attacks.count(), 30)
        self.assertEqual(
            set(attacks.values_list("family", flat=True)),
            {
                AttackItem.Family.LOCK,
                AttackItem.Family.INTERFERENCE,
                AttackItem.Family.DELAY,
                AttackItem.Family.SABOTAGE,
                AttackItem.Family.CONTROL,
                AttackItem.Family.COMBO,
            },
        )
        self.assertFalse(attacks.filter(price__lte=0).exists())


class InventoryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="carlos",
            password="pass12345",
        )
        self.ducky = Ducky.objects.create(owner=self.user, name="Byte")
        self.item = Item.objects.create(
            name="Gafas Hacker",
            item_type=Item.ItemType.EYES,
        )

    def test_inventory_item_relations(self):
        inventory_item = InventoryItem.objects.create(
            ducky=self.ducky,
            item=self.item,
        )
        self.assertIn(inventory_item, self.ducky.inventory.all())
        self.assertIn(inventory_item, self.item.owners.all())

    def test_ducky_item_pair_is_unique(self):
        InventoryItem.objects.create(ducky=self.ducky, item=self.item)
        with self.assertRaises(IntegrityError):
            InventoryItem.objects.create(ducky=self.ducky, item=self.item)
