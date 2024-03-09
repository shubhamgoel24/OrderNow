"""
Order test module
"""

from decimal import Decimal
from unittest.mock import ANY

from ddf import G
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import OrderItems, Orders
from restaurants.models import Menus, Restaurants
from users.models import Users


class CreateOrderTests(TestCase):
    """
    Class to test create order view
    """

    def setUp(self):
        self.user = G(Users, phone_number="7665672922")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant = G(Restaurants, owner=G(Users))
        self.menu_item1 = G(Menus, restaurant=self.restaurant)
        self.menu_item2 = G(Menus, restaurant=self.restaurant)

    def test_create_order_success(self):
        """
        Testcase for testing create order success case.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "data": {
                    "address": f"{self.user.street_address}, {self.user.city}, {self.user.state}, {self.user.zipcode}",
                    "contact": self.user.phone_number,
                    "customer": f"{self.user.id}",
                    "id": ANY,
                    "items": [
                        {
                            "id": ANY,
                            "item": self.menu_item1.name,
                            "price": self.menu_item1.price,
                            "quantity": data["items"][0]["quantity"],
                        }
                    ],
                    "order_datetime": ANY,
                    "restaurant": f"{self.restaurant.id}",
                    "status": "In Progress",
                    "total_amount": Decimal(self.menu_item1.price * data["items"][0]["quantity"]),
                },
                "status": "success",
                "message": None,
            },
        )

    def test_create_order_failure_without_items(self):
        """
        Testcase for testing create order failure case without items.
        """

        data = {"items": []}
        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"data": {"items": ["At least one item is required."]}, "message": None, "status": "error"}
        )

    def test_create_order_failure_when_user_phone_number_missing(self):
        """
        Testcase for testing create order failure case when user's phone number is missing.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        self.user.phone_number = None
        self.user.save()

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Profile": "Phone number is required for placing order. Please update it."},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_when_user_address_incomplete(self):
        """
        Testcase for testing create order failure case when user's address is incomplete.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        self.user.state = ""
        self.user.city = ""
        self.user.save()

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Profile": "Please update complete address first. Missing fields: state, city."},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_for_invalid_item_id(self):
        """
        Testcase for testing create order failure for invalid item id.
        """

        data = {"items": [{"id": "-1", "quantity": 1}]}

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Items": "Invalid item id: -1"},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_when_restaurant_is_inactive(self):
        """
        Testcase for testing create order failure case when restaurant is inactive.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        self.restaurant.is_active = False
        self.restaurant.save()

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Items": f"Invalid item id: {self.menu_item1.id}"},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_when_sufficient_items_quantity_not_available(self):
        """
        Testcase for testing create order failure case when sufficient items quantity is not available.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        self.menu_item1.quantity = 0
        self.menu_item1.save()

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Items": f"Not enough quantity available for item: {self.menu_item1.id}"},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_when_items_from_different_restaurant(self):
        """
        Testcase for testing create order failure case when items selected are from different restaurants.
        """

        restaurant = G(Restaurants, owner=G(Users))
        menu_item = G(Menus, restaurant=restaurant)

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}, {"id": menu_item.id, "quantity": 1}]}

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Items": "Select all items from same restaurant"},
                "status": "error",
                "message": None,
            },
        )

    def test_create_order_failure_when_user_balance_insufficient(self):
        """
        Testcase for testing create order failure case when user's balance is insufficient.
        """

        data = {"items": [{"id": self.menu_item1.id, "quantity": 1}]}
        self.user.balance = 0
        self.user.save()

        response = self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Profile": "Not enough balance"},
                "status": "error",
                "message": None,
            },
        )


class GetOrdersListTests(TestCase):
    """
    Class to test get orders view
    """

    maxDiff = None

    def setUp(self):
        self.user = G(Users)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.restaurant_owner = G(Users)
        self.restaurant = G(Restaurants, owner=self.restaurant_owner)

    def test_get_users_orders_success(self):
        """
        Testcase for fetching user's orders list success case.
        """

        order1 = G(Orders, restaurant=self.restaurant, customer=self.user)
        order1_item = G(OrderItems, order=order1)

        order2 = G(Orders, restaurant=self.restaurant, customer=self.user)
        order2_item1 = G(OrderItems, order=order2)
        order2_item2 = G(OrderItems, order=order2)

        response = self.client.get(
            reverse("orders:orders-list"),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {
                        "address": order1.address,
                        "contact": order1.contact,
                        "customer": f"{self.user.id}",
                        "id": order1.id,
                        "items": [
                            {
                                "id": order1_item.id,
                                "item": order1_item.item.name,
                                "price": order1_item.price,
                                "quantity": order1_item.quantity,
                            }
                        ],
                        "order_datetime": ANY,
                        "restaurant": f"{self.restaurant.id}",
                        "status": order1.status,
                        "total_amount": order1.total_amount,
                    },
                    {
                        "address": order2.address,
                        "contact": order2.contact,
                        "customer": f"{self.user.id}",
                        "id": order2.id,
                        "items": [
                            {
                                "id": order2_item1.id,
                                "item": order2_item1.item.name,
                                "price": order2_item1.price,
                                "quantity": order2_item1.quantity,
                            },
                            {
                                "id": order2_item2.id,
                                "item": order2_item2.item.name,
                                "price": order2_item2.price,
                                "quantity": order2_item2.quantity,
                            },
                        ],
                        "order_datetime": ANY,
                        "restaurant": f"{self.restaurant.id}",
                        "status": order2.status,
                        "total_amount": order2.total_amount,
                    },
                ],
                "status": "success",
                "message": None,
            },
        )

    def test_get_order_list_for_restaurant_owner(self):
        """
        Testcase for fetching orders list success case for restaurant owner.
        """

        order1 = G(Orders, restaurant=self.restaurant, customer=self.user)
        order1_item = G(OrderItems, order=order1)

        order2 = G(Orders, restaurant=self.restaurant, customer=self.user)
        order2_item1 = G(OrderItems, order=order2)
        order2_item2 = G(OrderItems, order=order2)

        other_restaurant = G(Restaurants, owner=self.user)
        other_order = G(Orders, restaurant=other_restaurant, customer=self.user)
        G(OrderItems, order=other_order)

        refresh = RefreshToken.for_user(self.restaurant_owner)

        response = self.client.get(
            reverse("orders:orders-list"),
            data={"restaurant_id": self.restaurant.id},
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {
                        "address": order1.address,
                        "contact": order1.contact,
                        "customer": f"{self.user.id}",
                        "id": order1.id,
                        "items": [
                            {
                                "id": order1_item.id,
                                "item": order1_item.item.name,
                                "price": order1_item.price,
                                "quantity": order1_item.quantity,
                            }
                        ],
                        "order_datetime": ANY,
                        "restaurant": f"{self.restaurant.id}",
                        "status": order1.status,
                        "total_amount": order1.total_amount,
                    },
                    {
                        "address": order2.address,
                        "contact": order2.contact,
                        "customer": f"{self.user.id}",
                        "id": order2.id,
                        "items": [
                            {
                                "id": order2_item1.id,
                                "item": order2_item1.item.name,
                                "price": order2_item1.price,
                                "quantity": order2_item1.quantity,
                            },
                            {
                                "id": order2_item2.id,
                                "item": order2_item2.item.name,
                                "price": order2_item2.price,
                                "quantity": order2_item2.quantity,
                            },
                        ],
                        "order_datetime": ANY,
                        "restaurant": f"{self.restaurant.id}",
                        "status": order2.status,
                        "total_amount": order2.total_amount,
                    },
                ],
                "status": "success",
                "message": None,
            },
        )
