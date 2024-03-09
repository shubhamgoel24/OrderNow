"""
Signals module
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import Users


@receiver(pre_save, sender=Users)
def add_full_name(sender, instance, *args, **kwargs):
    instance.full_name = instance.get_full_name()
