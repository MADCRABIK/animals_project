# Generated by Django 4.1 on 2022-08-11 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('good_hands', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animaltogoodhands',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
