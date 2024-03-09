# Generated by Django 3.2.23 on 2024-01-29 06:52

from django.db import migrations, models


def add_phone_numbers(apps, schema_editor):
    Users = apps.get_model("users", "Users")

    for user in Users.objects.all():
        user.full_name = f"{user.first_name} {user.last_name}".strip()
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_users_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="full_name",
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.RunPython(add_phone_numbers),
    ]
