from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from general_data.models import GeneralAnimalModel

# Create your models here.


class LostAnimal(GeneralAnimalModel):  # модель животного-потеряшки

    absolute_url = 'lost_detail'

    place = models.CharField(max_length=200, verbose_name='Где пропал(а)')
    time = models.CharField(max_length=200, verbose_name='Когда пропал(а)')
    special_signs = models.CharField(max_length=200, verbose_name='Особые приметы', blank=True)

    class Meta:
        verbose_name = 'Потерянное животное'
        verbose_name_plural = 'Потерянные животные'
