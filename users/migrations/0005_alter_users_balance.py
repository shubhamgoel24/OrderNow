# Generated by Django 3.2.23 on 2024-01-19 13:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_users_is_restaurant_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=9, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]