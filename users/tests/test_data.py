"""
Test data for users
"""

from random import randint

from ddf import N

from users.models import Users


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def get_random_user(**kwargs):
    user_data = N(
        Users, password=Users.objects.make_random_password(), phone_number=f"{random_with_N_digits(10)}", **kwargs
    )

    return {
        "username": user_data.username,
        "password": user_data.password,
        "email": user_data.email,
        "city": user_data.city,
        "state": user_data.state,
        "zipcode": user_data.zipcode,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "phone_number": user_data.phone_number,
        "street_address": user_data.street_address,
    }
