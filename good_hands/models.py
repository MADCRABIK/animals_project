from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from general_data.models import GeneralAnimalModel

# Create your models here.


class AnimalToGoodHands(GeneralAnimalModel):  # модель животного-потеряшки

    absolute_url = 'home'

    class Meta:
        verbose_name = 'Животное в добрые руки'
        verbose_name_plural = 'Животные в добрые руки'
