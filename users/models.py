from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import User, Department, Order

#User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET('Retired'))
    is_hod = models.BooleanField(default=False, null=False)
    is_pur = models.BooleanField(default=False, null=False)
    is_fin = models.BooleanField(default=False, null=False)
    is_gm = models.BooleanField(default=False, null=False)
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

LEVEL = [
    ('HOD', 'HOD'),
    ('PUR', 'PUR'),
    ('FIN', 'FIN'),
    ('GM', 'GM')
]

class Signature(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET(None),
        related_name='signatures'
        )
    level = models.CharField(choices=LEVEL, max_length=5, blank=True)
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
        level = self.level
        result = 'APPROVED' if self.approved else 'DECLINED'
        return (f'{order} - {user} as {level} - {result}')
