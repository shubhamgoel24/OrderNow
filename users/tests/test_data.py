"""
Test data for users
"""

from ddf import N

from users.models import Users


def get_random_user(**kwargs):
    user_data = N(Users, password=Users.objects.make_random_password(), **kwargs)

    return {
        "username": user_data.username,
        "password": user_data.password,
        "email": user_data.email,
        "city": user_data.city,
        "state": user_data.state,
        "zipcode": user_data.zipcode,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
    }
