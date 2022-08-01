# Generated by Django 4.0.6 on 2022-08-01 12:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost', '0003_lostanimal_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostanimal',
            name='phone_number',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
