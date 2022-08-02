# Generated by Django 4.0.6 on 2022-08-02 10:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип животного',
                'verbose_name_plural': 'Типы животных',
            },
        ),
        migrations.CreateModel(
            name='GeneralAnimalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Кличка')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(null=True, upload_to='photos/%Y-%m-d/', verbose_name='Фото')),
                ('phone_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('author', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='general_data.animaltype', verbose_name='Тип животного')),
            ],
            options={
                'verbose_name': 'Общая модель животных',
                'verbose_name_plural': 'Общие модели животных',
                'ordering': ['-published'],
            },
        ),
    ]