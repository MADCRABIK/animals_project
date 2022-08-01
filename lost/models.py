from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.


class LostAnimal(models.Model):  # модель животного-потеряшки
    objects = models.Manager()

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', editable=False, null=True)
    name = models.CharField(max_length=200, verbose_name='Кличка')
    type = models.ForeignKey('AnimalType', null=True, on_delete=models.PROTECT, verbose_name='Тип животного')
    photo = models.ImageField(upload_to='photos/%Y-%m-d/', verbose_name='Фото', null=True)
    place = models.CharField(max_length=200, verbose_name='Где пропал(а)')
    time = models.CharField(verbose_name='Когда пропал', blank=True, max_length=200)
    special_signs = models.CharField(max_length=200, verbose_name='Особые приметы', blank=True)
    description = models.TextField(verbose_name='Подробности')

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")  # валидатор для поля номера телефона
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=12)

    published = models.DateTimeField(verbose_name='Опубликовано', auto_now_add=True)

    class Meta:
        verbose_name = 'Пропавшее животное'
        verbose_name_plural = 'Пропавшие животные'
        ordering = ['-published']

    def get_absolute_url(self):
        return reverse('lost_detail', kwargs={'pk': self.pk})


class AnimalType(models.Model):  # возможные типы животных для выбора в 'type' в модели LostAnimal
    objects = models.Manager()

    name = models.CharField(max_length=200, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Тип животного'
        verbose_name_plural = 'Типы животных'

    def __str__(self):
        return self.name

