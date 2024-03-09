"""
Restaurants test module
"""

from unittest.mock import ANY
from django.test import TestCase
from django.urls import reverse
from ddf import G, N

from restaurants.models import Restaurants
from users.models import Users


class RestaurantCreationTests(TestCase):
    """
    Class to test restaurant creation view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_restaurant_creation_success(self):
        """
        Testcase for testing restaurant creation success case.
        """

        data = {"name": N(Restaurants).name}
        response = self.client.post(
            reverse("restaurants:restaurants-list"), data=data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        expected_data = {**data, "id": ANY}

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"data": expected_data, "status": "success", "message": None})
        self.assertDictEqual(
            {**expected_data, "is_active": True, "owner_id": self.user.id, "_state": ANY},
            Restaurants.objects.get(pk=response.json()["data"]["id"]).__dict__,
        )

    def test_restaurant_creation_validation_error(self):
        """
        Testcase for testing restaurant creation validation error case.
        """

        response = self.client.post(
            reverse("restaurants:restaurants-list"), data={}, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"data": {"name": ["This field is required."]}, "status": "error", "message": None}
        )

    def test_restaurant_creation_auth_error(self):
        """
        Testcase for testing restaurant creation without auth token case.
        """

        data = {"name": N(Restaurants).name}
        response = self.client.post(reverse("restaurants:restaurants-list"), data=data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )


class RestaurantRetrieveListTests(TestCase):
    """
    Class to test restaurant retrieve list view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_restaurant_retrieve_list_success(self):
        """
        Testcase for testing restaurant retrieve list success case.
        """

        r1 = G(Restaurants, owner=self.user)
        r2 = G(Restaurants, owner=self.user)
        G(Restaurants, owner=self.user, is_active=False)

        response = self.client.get(reverse("restaurants:restaurants-list"), HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": [{"id": r1.id, "name": r1.name}, {"id": r2.id, "name": r2.name}],
                "status": "success",
                "message": None,
            },
        )

    def test_restaurant_retrieve_list_auth_error(self):
        """
        Testcase for testing restaurant retrieve list without auth token case.
        """

        response = self.client.get(reverse("restaurants:restaurants-list"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )


class RestaurantRetrieveTests(TestCase):
    """
    Class to test restaurant retrieve view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_restaurant_retrieve_success(self):
        """
        Testcase for testing restaurant retrieve success case.
        """

        r1 = G(Restaurants, owner=self.user)

        response = self.client.get(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "data": {"id": r1.id, "name": r1.name},
                "status": "success",
                "message": None,
            },
        )

    def test_restaurant_retrieve_auth_error(self):
        """
        Testcase for testing restaurant retrieve without auth token case.
        """

        r1 = G(Restaurants, owner=self.user)
        response = self.client.get(reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )

    def test_restaurant_retrieve_failure_for_deleted(self):
        """
        Testcase for testing restaurant retrieve failure case when restaurant is deleted.
        """

        r1 = G(Restaurants, owner=self.user, is_active=False)

        response = self.client.get(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "data": None,
                "status": "error",
                "message": "Not found.",
            },
        )


class RestaurantDeleteTests(TestCase):
    """
    Class to test restaurant delete view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_restaurant_delete_success(self):
        """
        Testcase for testing restaurant delete success case.
        """

        r1 = G(Restaurants, owner=self.user)

        response = self.client.delete(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 204)
        self.assertDictEqual(
            {"id": r1.id, "name": r1.name, "is_active": False, "owner_id": self.user.id, "_state": ANY},
            Restaurants.objects.get(pk=r1.id).__dict__,
        )

    def test_restaurant_delete_auth_error(self):
        """
        Testcase for testing restaurant delete without auth token case.
        """

        r1 = G(Restaurants, owner=self.user)
        response = self.client.delete(reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )

    def test_restaurant_delete_failure_for_deleted_restaurant(self):
        """
        Testcase for testing restaurant delete failure case when restaurant is deleted.
        """

        r1 = G(Restaurants, owner=self.user, is_active=False)

        response = self.client.delete(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "data": None,
                "status": "error",
                "message": "Not found.",
            },
        )


class RestaurantUpdateTests(TestCase):
    """
    Class to test restaurant update view
    """

    def setUp(self):
        password = Users.objects.make_random_password()
        self.user = N(Users)
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(reverse("users:login"), data={"email": self.user.email, "password": password})
        self.token = response.data["access"]

    def test_restaurant_update_success(self):
        """
        Testcase for testing restaurant update success case.
        """

        r1 = G(Restaurants, owner=self.user)

        response = self.client.patch(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}),
            data={"name": "newName"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"data": {"id": r1.id, "name": "newName"}, "status": "success", "message": None}
        )
        self.assertDictEqual(
            {"id": r1.id, "name": "newName", "is_active": True, "owner_id": self.user.id, "_state": ANY},
            Restaurants.objects.get(pk=r1.id).__dict__,
        )

    def test_restaurant_update_auth_error(self):
        """
        Testcase for testing restaurant update without auth token case.
        """

        r1 = G(Restaurants, owner=self.user)
        response = self.client.patch(reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"data": None, "status": "error", "message": "Authentication credentials were not provided."},
        )

    def test_restaurant_update_failure_for_deleted_restaurant(self):
        """
        Testcase for testing restaurant update failure case when restaurant is deleted.
        """

        r1 = G(Restaurants, owner=self.user, is_active=False)

        response = self.client.patch(
            reverse("restaurants:restaurants-detail", kwargs={"pk": r1.id}), HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "data": None,
                "status": "error",
                "message": "Not found.",
            },
        )
