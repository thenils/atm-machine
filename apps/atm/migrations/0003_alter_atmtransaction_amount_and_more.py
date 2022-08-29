# Generated by Django 4.1 on 2022-08-27 21:47

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0002_alter_atmtransaction_expiredat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmtransaction',
            name='amount',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='atmtransaction',
            name='expiredAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 21, 52, 58, 26363, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='atmtransaction',
            name='transaction_id',
            field=models.CharField(default='08/27/202221:47:58', editable=False, max_length=24, unique=True),
        ),
    ]
