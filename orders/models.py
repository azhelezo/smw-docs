from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Department(models.Model):
    code = models.CharField(
        default='NA',
        null=False,
        blank=False,
        max_length=5
        )
    name = models.CharField(
        default='Not assigned',
        null=False,
        blank=False,
        max_length=50
        )

    def __str__(self):
        return str(self.name)

class Signature(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET(None),
        related_name='signatures'
        )
    approved = models.BooleanField(default=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    win_username = models.CharField(default=None, null=False, max_length=200)
    win_pcname = models.CharField(default=None, null=False, max_length=200)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False, verbose_name='Заказ')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name='К оплате',
        help_text='включая 20% НДС'
        )
    requested_by = models.ForeignKey(
        User, 
        on_delete=models.SET(None),
        related_name='orders'
        )
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET(None),
        related_name='orders'
        )
    date_created = models.DateTimeField('date created', auto_now_add=True)
    all_signed = models.BooleanField(null=True)
    hod_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET(None),
        related_name='order_hod',
        default=None,
        blank=True, null=True,
        )
    pur_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET(None),
        related_name='order_pur',
        default=None,
        blank=True, null=True,
        )
    fin_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET(None),
        related_name='order_fin',
        default=None,
        blank=True, null=True,
        )
    gm_signature = models.ForeignKey(
        Signature,
        on_delete=models.SET(None),
        related_name='order_gm',
        default=None,
        blank=True, null=True,
        )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date_created']
