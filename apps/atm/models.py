import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.account.models import ATMCard


def get_cash_details():
    """
    notes in 100, 200, 500,2000
    """
    return {
        '100': 0,
        '200': 0,
        '500': 0,
        '2000': 0
    }


# Create your models here.
class ATM(models.Model):
    bank = models.CharField(max_length=25)
    city = models.CharField(max_length=55)
    code = models.IntegerField(default=0)
    atm_code = models.CharField(max_length=65, default='mycode')
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=7, decimal_places=0, default=0, validators=[
        MaxValueValidator(2000000)
    ])
    in_cash = models.JSONField(default=get_cash_details())

    def __str__(self):
        return f'{self.bank} balance: {self.balance}'


class ATMTransaction(models.Model):
    types = (
        ('C', 'Credit'),
        ('D', 'Debit')
    )
    status_level = (
        ('SUCCESS', 'Success'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed')
    )
    type = models.CharField(max_length=1, default='C', choices=types)
    transaction_id = models.CharField(
        max_length=24,
        default=str(uuid.uuid4()),
        editable=False,
        unique=True
    )
    amount = models.IntegerField(null=True, validators=[
        MaxValueValidator(10000),
        MinValueValidator(100)
    ])
    card = models.ForeignKey(ATMCard, on_delete=models.DO_NOTHING, related_name='my_transactions')
    atm = models.ForeignKey(ATM, on_delete=models.DO_NOTHING, related_name='atm_transactions')
    success = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default='PENDING', choices=status_level)
    in_cash = models.JSONField(default=get_cash_details())
    createdAt = models.DateTimeField(auto_now=True)
    expiredAt = models.DateTimeField(default=timezone.now()+timezone.timedelta(minutes=5))

    def __str__(self):
        return f'{self.transaction_id} status:{self.status} amount:{self.amount}'

