import uuid

from django.db import models
from django.utils import timezone

from apps.account.models import ATMCard
from apps.atm.models import ATM


# Create your models here.

class CardToken(models.Model):
    card = models.ForeignKey(ATMCard, on_delete=models.DO_NOTHING)
    atm = models.ForeignKey(ATM, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    is_validate = models.BooleanField(default=False)
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    expireAt = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=3))

    def __str__(self):
        return f'{self.key}'
