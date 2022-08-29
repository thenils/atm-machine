from django.db import models
from django.utils import timezone


class BankAccount(models.Model):
    number = models.CharField(
        max_length=12,
        unique=True
    )
    phone = models.CharField(
        max_length=12
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Acc No. {self.number}, balance: {self.balance}'


class ATMCard(models.Model):
    STATUS = (
        ('active', 'active'),
        ('deactivated', 'deactivated')
    )

    number = models.CharField(
        max_length=16,
        unique=True,
    )
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.DO_NOTHING,
        verbose_name="bank account",
        related_name='atm_account',
    )
    pin = models.CharField(
        max_length=4
    )
    name = models.CharField(
        max_length=35
    )
    card_status = models.CharField(default='deactivated', max_length=11, choices=STATUS)

    date_issued = models.DateField(
        default=timezone.now
    )
    expire_date = models.DateField(
        default=timezone.now() + timezone.timedelta(days=1460)  # 4 year after issued
    )

    def __str__(self):
        return f'Card No. {self.number}, status: {self.card_status}'

