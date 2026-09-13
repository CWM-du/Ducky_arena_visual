from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from duckies.models import Ducky, InventoryItem, Item

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
