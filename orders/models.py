from django.contrib.auth import get_user_model
from django.db import models
from users.models import Signature

User = get_user_model()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_by = models.ForeignKey(
        Signature, 
        on_delete=models.SET('Retired'),
        related_name='orders'
        )
    date_created = models.DateTimeField('date created', auto_now_add=True)
    hod_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET('Retired'),
        related_name='hod_signature',
        default=None,
        blank=True, null=True,
        )
    pur_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET('Retired'),
        related_name='pur_signature',
        default=None,
        blank=True, null=True,
        )
    fin_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET('Retired'),
        related_name='fin_signature',
        default=None,
        blank=True, null=True,
        )
    gm_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET('Retired'),
        related_name='gm_signature',
        default=None,
        blank=True, null=True,
        )
    all_signed = models.BooleanField(null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date_created']