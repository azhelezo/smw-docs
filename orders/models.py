from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    requested_by = models.ForeignKey(
        User, 
        on_delete=models.SET('Retired'),
        related_name='orders'
        )
    date_created = models.DateTimeField('date created', auto_now_add=True)
    hod_approved = models.BooleanField(null=True)
    hod_user = models.ForeignKey(
        User,
        on_delete=models.SET('Retired'),
        related_name='hod_approved',
        blank=True, null=True,
        )
    pur_approved = models.BooleanField(null=True)
    pur_user = models.ForeignKey(
        User,
        on_delete=models.SET('Retired'),
        related_name='pur_approved',
        blank=True, null=True,
        )
    fin_approved = models.BooleanField(null=True)
    fin_user = models.ForeignKey(
        User,
        on_delete=models.SET('Retired'),
        related_name='fin_approved',
        blank=True, null=True,
        )
    gm_approved = models.BooleanField(null=True)
    gm_user = models.ForeignKey(
        User,
        on_delete=models.SET('Retired'),
        related_name='gm_approved',
        default=None,
        blank=True, null=True,
        )
    all_approved = models.BooleanField(null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date_created']