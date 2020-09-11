from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

DEPARTMENTS = [
    ('EN', 'Engineering'),
    ('FI', 'Finance'),
    ('FB', 'Food and Beverage'),
    ('RD', 'Rooms Division'),
    ('SM', 'Sales and Marketing'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET('Retired'))
    is_hod = models.BooleanField(default=False, null=False)
    is_pur = models.BooleanField(default=False, null=False)
    is_fin = models.BooleanField(default=False, null=False)
    is_gm = models.BooleanField(default=False, null=False)
    department = models.CharField(choices=DEPARTMENTS, default='Not assigned', max_length=100)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()