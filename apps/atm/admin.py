from django.contrib import admin

# Register your models here.
from .models import ATM, ATMTransaction

admin.site.register(ATM)
admin.site.register(ATMTransaction)
