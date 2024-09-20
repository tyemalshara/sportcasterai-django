from django.contrib import admin
from .models import UserPayment

class UserPaymentAdmin(admin.ModelAdmin):
  list_display = ('app_user', 'payment_bool', 'stripe_checkout_id',)

admin.site.register(UserPayment, UserPaymentAdmin)
