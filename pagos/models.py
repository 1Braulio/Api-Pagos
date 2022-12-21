from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
# Create your models here.

class PagosV1(models.Model):
    class Servicios(models.TextChoices):
        NETFLIX = 'NF', _('Netflix')
        AMAZON = 'AP', _('Amazon Video')
        START = 'ST', _('Start+')
        PARAMOUNT = 'PM', _('Paramount+')

    servicio = models.CharField(
        max_length=2,
        choices=Servicios.choices,
        default=Servicios.NETFLIX,
    )
    fecha_pago = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete =models.CASCADE, related_name='users')
    monto = models.FloatField(default=0.0)


class Services(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    Logo = models.CharField(max_length=1000)

class ExpiredPayments(models.Model):
    payment_user_id = models.ForeignKey(User, on_delete =models.CASCADE, related_name='expired_payments_users')
    penalty_fee_amount = models.FloatField()

class PaymentUser(models.Model):
    user_id = models.ForeignKey(User, on_delete =models.CASCADE, related_name='payment_users')
    service_id = models.ForeignKey(Services, on_delete =models.CASCADE, related_name='services')
    amount = models.FloatField()
    payment_date = models.DateTimeField()
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        
        if self.expiration_date < self.payment_date:
            ExpiredPayments.create(payment_user_id = self.user_id,  penalty_fee_amount = 10)

        super().save(*args, **kwargs)
    