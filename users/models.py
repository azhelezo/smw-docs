from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Department

User = get_user_model()


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


'''
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='signatures'
        )
'''