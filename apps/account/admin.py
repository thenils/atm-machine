from django.contrib import admin

# Register your models here.
from .models import BankAccount, ATMCard

admin.site.register(BankAccount)
admin.site.register(ATMCard)