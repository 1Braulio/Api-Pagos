from django.contrib import admin
from .models import Services, ExpiredPayments, PaymentUser

# Register your models here.

admin.site.register(Services)
admin.site.register(ExpiredPayments)
admin.site.register(PaymentUser)