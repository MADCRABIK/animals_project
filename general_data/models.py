from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Create your models here

# ОБЩАЯ МОДЕЛЬ "ТИПЫ ЖИВОТНЫХ"
class AnimalType(models.Model):  # возможные типы животных для выбора в 'type' в модели LostAnimal
    objects = models.Manager()

    name = models.CharField(max_length=200, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Тип животного'
        verbose_name_plural = 'Типы животных'

    def __str__(self):
        return self.name


# ОБЩАЯ МОДЕЛЬ ЖИВОТНЫХ (ОБЪЯВЛЕНИЙ) | СОЗДАНА ДЛЯ ДАЛЬНЕЙШЕГО РАСШИРЕНИЯ
class GeneralAnimalModel(models.Model):
    objects = models.Manager()

    absolute_url = 'home'  # НЕОБХОДИМО ПЕРЕОПРЕДЕЛИТЬ ДЛЯ РАБОТЫ МЕТОДА GET_ABSOLUTE_URL

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', editable=False, null=True)
    type = models.ForeignKey(AnimalType, on_delete=models.PROTECT, verbose_name='Тип животного')
    name = models.CharField(max_length=200, verbose_name='Кличка')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")  # валидатор для поля номера телефона
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=12, verbose_name='Телефон для связи')

    published = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    moderated = models.BooleanField(default=False, verbose_name='Прошло модерацию')

    class Meta:
        verbose_name = 'Общая модель животных'
        verbose_name_plural = 'Общие модели животных'
        ordering = ['-published']
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(self.absolute_url)
