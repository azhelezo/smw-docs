from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Department, Order
from multiselectfield import MultiSelectField

User = get_user_model()

LEVEL = [  # define employee levels
    (0, 'Head of Department'),
    (1, 'Purchasing Manager'),
    (2, 'Financial Controller'),
    (3, 'General Manager')
]

LEVEL_TITLE = [x for x, y in LEVEL]  # list of level titles only

LEVEL_VIEW_ALL = [1, 2, 3, ]  # list of levels to view all requests

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET('Retired'))
    sign_as = MultiSelectField(choices=LEVEL, default=None, null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET('Retired'),
        related_name='profiles',
        blank=True, null=True,
        )

    def __str__(self):
        return f'{self.user} - Profile'

    @classmethod
    def create(profile, user, department=None):
        if department == None:
            if not Department.objects.all().exists():
                department = Department.objects.create(
                    code='NA',
                    name='Not assigned')
        profile = profile(user=user, department=department)
        return profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Signature(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET(None),
        related_name='signatures'
        )
    level = models.CharField(choices=LEVEL, max_length=5)
    order =  models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='signatures'
        )
    approved = models.BooleanField(default=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    win_username = models.CharField(default=None, null=False, max_length=200)
    win_pcname = models.CharField(default=None, null=False, max_length=200)

    def __str__(self):
        order = self.order.id
        user = self.user
        level = LEVEL[int(self.level)][1]
        result = 'APPROVED' if self.approved else 'DECLINED'
        return (f'{order} - {user} as {level} - {result}')
