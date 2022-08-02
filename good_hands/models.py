from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from lost.models import AnimalType

# Create your models here.


class AnimalToGoodHands(models.Model):
    objects = models.Manager()

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', editable=False, null=True)
    type = models.ForeignKey(AnimalType, on_delete=models.PROTECT, verbose_name='Тип животного')
    name = models.CharField(max_length=200, verbose_name='Кличка')
    description = models.TextField(verbose_name='Описание')

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")  # валидатор для поля номера телефона
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=12)

    published = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Животное в добрые руки'
        verbose_name_plural = 'Животные в добрые руки'
        ordering = ['-published']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('good_hands_detail', kwargs={'pk': self.pk})
