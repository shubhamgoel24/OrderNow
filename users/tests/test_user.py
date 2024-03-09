"""
Users test module
"""

from decimal import Decimal
from unittest.mock import ANY
from django.test import TestCase
from django.urls import reverse
from ddf import G, N

from users.models import Users
from users.tests.test_data import get_random_user


class UsersRegistrationTests(TestCase):
    """
    Class to test user registration view
    """

    def test_user_registration_success(self):
        """
        Testcase for testing user registration success case.
        """

        user_data = get_random_user()
        response = self.client.post(reverse("users:users"), data=user_data)

        expected_data = {**user_data, "id": ANY, "balance": 1000.00}
        del expected_data["password"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})
        self.assertDictContainsSubset(
            {**expected_data, "balance": Decimal("1000.00")},
            Users.objects.get(pk=response.json()["data"]["id"]).__dict__,
        )

    def test_user_registration_validation_error(self):
        """
        Testcase for testing user registration for validation error.
        """

        invalid_user_data = get_random_user(email="invalidemail")
        response = self.client.post(reverse("users:users"), data=invalid_user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"data": {"email": ["Enter a valid email address."]}, "status": "error", "message": None},
        )

    def test_user_registration_success_when_balance_is_provided(self):
        """
        Testcase for testing user registration success case when balance is sent.
        """

        user_data_with_balance = get_random_user()
        user_data_with_balance["balance"] = 10000
        response = self.client.post(reverse("users:users"), data=user_data_with_balance)

        expected_data = {**user_data_with_balance, "id": ANY, "balance": 10000.00}
        del expected_data["password"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})
        self.assertDictContainsSubset(
            {**expected_data, "balance": Decimal("10000.00")},
            Users.objects.get(pk=response.json()["data"]["id"]).__dict__,
        )

    def test_user_registration_email_already_exists(self):
        """
        Testcase for testing user registration for email exists error.
        """

        existing_user = G(Users)
        user_data = get_random_user(email=existing_user.email)
        response = self.client.post(reverse("users:users"), data=user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "data": {"email": ["A user with that email already exists."]},
                "status": "error",
                "message": None,
            },
        )


class UsersLoginTests(TestCase):
    """
    Class to test user login view
    """

    def test_user_login_success(self):
        """
        Testcase for testing user login success case.
        """

        password = Users.objects.make_random_password()
        user = N(Users)
        user.set_password(password)
        user.save()
        response = self.client.post(reverse("users:login"), data={"email": user.email, "password": password})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"data": {"access": ANY, "refresh": ANY}, "status": "success", "message": None},
        )

    def test_user_login_failure(self):
        """
        Testcase for testing user login failure case.
        """

        password = Users.objects.make_random_password()
        user = N(Users)
        user.set_password(password)
        user.save()
        response = self.client.post(reverse("users:login"), data={"email": "email", "password": "password"})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "data": None,
                "status": "error",
                "message": "No active account found with the given credentials",
            },
        )


class UsersRetrieveTests(TestCase):
    """
    Class to test get user view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_user_get_details_success(self):
        """
        Testcase for testing user get details success.
        """

        response = self.client.get(reverse("users:users"), HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [
                    {
                        "username": self.user.username,
                        "id": self.user.id,
                        "email": self.user.email,
                        "city": self.user.city,
                        "state": self.user.state,
                        "zipcode": self.user.zipcode,
                        "first_name": self.user.first_name,
                        "last_name": self.user.last_name,
                        "balance": float(self.user.balance),
                    }
                ],
                "status": "success",
                "message": None,
            },
        )

    def test_user_get_details_without_auth(self):
        """
        Testcase for testing user get details failure when auth credentials are not provided.
        """

        response = self.client.get(reverse("users:users"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )


class UsersDeleteTests(TestCase):
    """
    Class to test delete user view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_user_delete_success(self):
        """
        Testcase for testing user delete success.
        """

        response = self.client.delete(
            reverse("users:users", kwargs={"pk": self.user.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Users.objects.get(pk=self.user.id).is_active, False)

    def test_user_delete_without_auth(self):
        """
        Testcase for testing user delete failure when auth credentials are not provided.
        """

        response = self.client.delete(reverse("users:users", kwargs={"pk": self.user.id}))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )

    def test_user_delete_failure_when_incorrect_id_is_provided(self):
        """
        Testcase for testing user delete failure when id of another user is provided.
        """

        another_user = G(Users)
        response = self.client.delete(
            reverse("users:users", kwargs={"pk": another_user.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Not found."},
        )


class UsersUpdateTests(TestCase):
    """
    Class to test update user view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_user_update_success(self):
        """
        Testcase for testing user update success.
        """

        response = self.client.patch(
            reverse("users:users", kwargs={"pk": self.user.id}),
            {"first_name": "Test"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": {
                    "username": self.user.username,
                    "id": self.user.id,
                    "email": self.user.email,
                    "city": self.user.city,
                    "state": self.user.state,
                    "zipcode": self.user.zipcode,
                    "first_name": "Test",
                    "last_name": self.user.last_name,
                    "balance": float(self.user.balance),
                },
                "status": "success",
                "message": None,
            },
        )
        self.assertEqual(Users.objects.get(pk=self.user.id).first_name, "Test")

    def test_user_update_without_auth(self):
        """
        Testcase for testing user update failure when auth credentials are not provided.
        """

        response = self.client.patch(reverse("users:users", kwargs={"pk": self.user.id}))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )

    def test_user_update_failure_when_incorrect_id_is_provided(self):
        """
        Testcase for testing user update failure when id of another user is provided.
        """

        another_user = G(Users)
        response = self.client.patch(
            reverse("users:users", kwargs={"pk": another_user.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Not found."},
        )
