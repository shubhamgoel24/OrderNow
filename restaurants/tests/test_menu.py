"""
Menu test module
"""

from decimal import Decimal
from unittest.mock import ANY

from ddf import G, N
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from restaurants.models import Menus, Restaurants
from users.models import Users


class MenuAddItemTests(TestCase):
    """
    Class to test menu add item view
    """

    def setUp(self):
        self.user = G(Users)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant = G(Restaurants, owner=self.user)

        menu_data = N(Menus)
        self.menu_data = {"name": menu_data.name, "price": Decimal(menu_data.price), "quantity": menu_data.quantity}

    def test_menu_add_item_success(self):
        """
        Testcase for testing menu add item success.
        """

        data = self.menu_data
        response = self.client.post(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": self.restaurant.id}),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        expected_data = {**data, "price": Decimal(data["price"]), "id": ANY}

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})
        self.assertDictEqual(
            {**expected_data, "restaurant_id": self.restaurant.id, "_state": ANY},
            Menus.objects.get(pk=response.json()["data"]["id"]).__dict__,
        )

    def test_menu_add_item_validation_error(self):
        """
        Testcase for testing menu add item validation error.
        """

        data = {"price": -1, "quantity": 10}

        response = self.client.post(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": self.restaurant.id}),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {
                    "name": ["This field is required."],
                    "price": ["Ensure this value is greater than or equal to 0."],
                },
                "status": "error",
                "message": None,
            },
        )

    def test_menu_add_item_for_invalid_restaurant_id(self):
        """
        Testcase for testing menu add item success.
        """

        another_user = G(Users)
        another_restaurant = G(Restaurants, owner=another_user)

        data = self.menu_data
        response = self.client.post(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": another_restaurant.id}),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "You do not have permission to perform this action."},
        )


class MenuDeleteItemTests(TestCase):
    """
    Class to test menu delete item view
    """

    def setUp(self):
        self.user = G(Users)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant = G(Restaurants, owner=self.user)

    def test_menu_delete_not_allowed(self):
        """
        Testcase for testing menu delete item not allowed.
        """

        item = G(Menus, restaurant=self.restaurant)

        response = self.client.delete(
            reverse("restaurants:menus-detail", kwargs={"restaurant_id": self.restaurant.id, "pk": item.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "DELETE method is not allowed for this resource."},
        )


class GetMenuItemsListTests(TestCase):
    """
    Class to test get menu items list view
    """

    def setUp(self):
        self.user = G(Users)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant = G(Restaurants, owner=self.user)
        self.item1 = G(Menus, restaurant=self.restaurant)
        self.item2 = G(Menus, restaurant=self.restaurant)

    def test_get_menu_list_success(self):
        """
        Testcase for testing get menu list success.
        """

        response = self.client.get(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": self.restaurant.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        expected_data = [
            {"id": self.item1.id, "name": self.item1.name, "price": self.item1.price, "quantity": self.item1.quantity},
            {"id": self.item2.id, "name": self.item2.name, "price": self.item2.price, "quantity": self.item2.quantity},
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})

    def test_get_menu_list_for_invalid_restaurant_id(self):
        """
        Testcase for testing get menu list invalid id.
        """

        response = self.client.post(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": -1}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "You do not have permission to perform this action."},
        )

    def test_get_menu_list_by_anyone(self):
        """
        Testcase for testing get menu list success for any user.
        """

        another_user = G(Users)
        refresh = RefreshToken.for_user(another_user)
        token = str(refresh.access_token)

        response = self.client.get(
            reverse("restaurants:menus-list", kwargs={"restaurant_id": self.restaurant.id}),
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        expected_data = [
            {"id": self.item1.id, "name": self.item1.name, "price": self.item1.price, "quantity": self.item1.quantity},
            {"id": self.item2.id, "name": self.item2.name, "price": self.item2.price, "quantity": self.item2.quantity},
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})


class UpdateMenuItemTests(TestCase):
    """
    Class to test update menu item view
    """

    def setUp(self):
        self.user = G(Users)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant = G(Restaurants, owner=self.user)
        self.item = G(Menus, restaurant=self.restaurant)

    def test_update_menu_item_success(self):
        """
        Testcase for testing update menu item success.
        """

        response = self.client.patch(
            reverse("restaurants:menus-detail", kwargs={"restaurant_id": self.restaurant.id, "pk": self.item.id}),
            data={"quantity": 567, "price": 890.80},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        expected_data = {"id": self.item.id, "name": self.item.name, "price": 890.8, "quantity": 567}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})

    def test_update_menu_list_by_anyone_failure(self):
        """
        Testcase for testing update menu failure for user that is not owner of restaurant.
        """

        another_user = G(Users)
        refresh = RefreshToken.for_user(another_user)
        token = str(refresh.access_token)

        response = self.client.patch(
            reverse("restaurants:menus-detail", kwargs={"restaurant_id": self.restaurant.id, "pk": self.item.id}),
            data={"quantity": 567, "price": 890.80},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "You do not have permission to perform this action."},
        )
