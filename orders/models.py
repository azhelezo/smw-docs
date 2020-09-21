from django.contrib.auth import get_user_model
from django.db import models
# from users.models import Signature

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

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False, verbose_name='Заказ')
    supplier = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Поставщик')
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
        related_name='orders',
        verbose_name='Отдел'
        )
    date_created = models.DateTimeField('date created', auto_now_add=True)
    declined = models.BooleanField(default=False)
    all_signed = models.BooleanField(null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-date_created']
