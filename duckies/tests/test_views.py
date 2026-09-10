from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from duckies.models import Ducky, InventoryItem, Item

User = get_user_model()


class DuckyViewTests(TestCase):
    def setUp(self):
        self.carlos = User.objects.create_user(
            username="carlos",
            password="pass12345",
        )
        self.laura = User.objects.create_user(
            username="laura",
            password="pass12345",
        )
        self.carlos_ducky = Ducky.objects.create(
            owner=self.carlos,
            name="Byte",
        )
        self.laura_ducky = Ducky.objects.create(
            owner=self.laura,
            name="Quack",
        )
        self.item = Item.objects.create(
            name="Sombrero Python",
            item_type=Item.ItemType.HEAD,
        )
        self.carlos_inventory = InventoryItem.objects.create(
            ducky=self.carlos_ducky,
            item=self.item,
        )
        self.laura_inventory = InventoryItem.objects.create(
            ducky=self.laura_ducky,
            item=self.item,
        )

    def test_anonymous_user_cannot_access_ducky(self):
        response = self.client.get(reverse("duckies:my_ducky"))
        self.assertEqual(response.status_code, 302)

    def test_user_sees_only_own_inventory(self):
        self.client.login(username="carlos", password="pass12345")
        response = self.client.get(reverse("duckies:inventory"))
        self.assertContains(response, "Sombrero Python")
        self.assertEqual(response.context["ducky"], self.carlos_ducky)
        self.assertNotEqual(response.context["ducky"], self.laura_ducky)

    def test_user_cannot_equip_another_users_item(self):
        self.client.login(username="carlos", password="pass12345")
        response = self.client.post(
            reverse("duckies:equip", args=[self.laura_inventory.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.laura_inventory.refresh_from_db()
        self.assertFalse(self.laura_inventory.equipped)

    def test_user_cannot_unequip_another_users_item(self):
        self.laura_inventory.equipped = True
        self.laura_inventory.save(update_fields=["equipped"])

        self.client.login(username="carlos", password="pass12345")
        response = self.client.post(
            reverse("duckies:unequip", args=[self.laura_inventory.pk])
        )
        self.assertEqual(response.status_code, 404)

        self.laura_inventory.refresh_from_db()
        self.assertTrue(self.laura_inventory.equipped)

    def test_equipment_requires_post(self):
        self.client.login(username="carlos", password="pass12345")
        response = self.client.get(
            reverse("duckies:equip", args=[self.carlos_inventory.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.carlos_inventory.refresh_from_db()
        self.assertFalse(self.carlos_inventory.equipped)

    def test_rename_requires_valid_name(self):
        self.client.login(username="carlos", password="pass12345")

        response = self.client.post(
            reverse("duckies:rename"),
            {"name": "x"},
        )
        self.assertEqual(response.status_code, 200)
        self.carlos_ducky.refresh_from_db()
        self.assertEqual(self.carlos_ducky.name, "Byte")

        response = self.client.post(
            reverse("duckies:rename"),
            {"name": "Byte Prime"},
        )
        self.assertRedirects(response, reverse("duckies:my_ducky"))
        self.carlos_ducky.refresh_from_db()
        self.assertEqual(self.carlos_ducky.name, "Byte Prime")

    def test_inventory_filter(self):
        body_item = Item.objects.create(
            name="Armadura SQL",
            item_type=Item.ItemType.BODY,
        )
        InventoryItem.objects.create(
            ducky=self.carlos_ducky,
            item=body_item,
        )

        self.client.login(username="carlos", password="pass12345")
        response = self.client.get(
            reverse("duckies:inventory"),
            {"type": "BODY"},
        )
        inventory = list(response.context["inventory"])
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0].item, body_item)
