"""
Reports test module
"""

from datetime import datetime, timedelta
from decimal import Decimal
from random import randint

from ddf import G
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Orders
from restaurants.models import Menus, Restaurants
from users.models import Users


class ReportsViewTests(TestCase):
    """
    Class to test restaurant reports viewset
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = G(Users)
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.restaurant = G(Restaurants, owner=cls.user)
        cls.item1 = G(Menus, restaurant=cls.restaurant, quantity=100)
        cls.item2 = G(Menus, restaurant=cls.restaurant, quantity=100)

    def test_customer_spends_report(self):
        """
        Testcase for customer spends report.
        """

        user1 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}, {"id": self.item2.id, "quantity": 2}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user1).access_token}",
        )

        user2 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user2).access_token}",
        )

        response = self.client.get(
            reverse("restaurants:reports-customer-spends-report", kwargs={"restaurant_id": self.restaurant.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {
                        "total_amount_spent": Decimal((self.item1.price * 1) + (self.item2.price * 2)),
                        "user_email": user1.email,
                    },
                    {"total_amount_spent": Decimal(self.item1.price * 1), "user_email": user2.email},
                ],
                "status": "success",
                "message": None,
            },
        )

    def test_customer_spends_report_with_date_range(self):
        """
        Testcase for customer spends report with date range.
        """

        user1 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}, {"id": self.item2.id, "quantity": 2}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user1).access_token}",
        )
        G(
            Orders,
            restaurant=self.restaurant,
            customer=user1,
            order_datetime=datetime.now() - timedelta(days=10),
            total_amount=10,
        )

        user2 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user2).access_token}",
        )

        response = self.client.get(
            reverse("restaurants:reports-customer-spends-report", kwargs={"restaurant_id": self.restaurant.id}),
            data={
                "from_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "to_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            },
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {
                        "total_amount_spent": Decimal((self.item1.price * 1) + (self.item2.price * 2)),
                        "user_email": user1.email,
                    },
                    {"total_amount_spent": Decimal(self.item1.price * 1), "user_email": user2.email},
                ],
                "status": "success",
                "message": None,
            },
        )

    def test_customer_spends_report_with_date_range_validation_error(self):
        """
        Testcase for customer spends report with date range validation error when complete range is not given.
        """

        response = self.client.get(
            reverse("restaurants:reports-customer-spends-report", kwargs={"restaurant_id": self.restaurant.id}),
            data={
                "from_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            },
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"Params": ["Please provide both 'from_date' and 'to_date'"]},
                "status": "error",
                "message": None,
            },
        )

    def test_item_popularity_report(self):
        """
        Testcase for item popularity report.
        """

        user1 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}, {"id": self.item2.id, "quantity": 2}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user1).access_token}",
        )

        user2 = G(Users, phone_number=randint(1000000000, 9999999999))
        data = {"items": [{"id": self.item1.id, "quantity": 1}]}
        self.client.post(
            reverse("orders:orders-list"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user2).access_token}",
        )

        response = self.client.get(
            reverse("restaurants:reports-item-popularity-report", kwargs={"restaurant_id": self.restaurant.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [{"item": self.item2.id, "orders": 1}, {"item": self.item1.id, "orders": 2}],
                "status": "success",
                "message": None,
            },
        )

    def test_customer_favorites_report(self):
        """
        Testcase for customer favorites report.
        """

        user1 = G(Users, phone_number=randint(1000000000, 9999999999))
        self.client.post(
            reverse("orders:orders-list"),
            data={"items": [{"id": self.item1.id, "quantity": 1}, {"id": self.item2.id, "quantity": 2}]},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user1).access_token}",
        )
        self.client.post(
            reverse("orders:orders-list"),
            data={"items": [{"id": self.item2.id, "quantity": 1}]},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user1).access_token}",
        )

        user2 = G(Users, phone_number=randint(1000000000, 9999999999))
        self.client.post(
            reverse("orders:orders-list"),
            data={"items": [{"id": self.item1.id, "quantity": 1}]},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user2).access_token}",
        )

        response = self.client.get(
            reverse("restaurants:reports-customer-favorites-report", kwargs={"restaurant_id": self.restaurant.id}),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {"email": user1.email, "item_count": 2, "item_id": self.item2.id},
                    {"email": user2.email, "item_count": 1, "item_id": self.item1.id},
                ],
                "status": "success",
                "message": None,
            },
        )
