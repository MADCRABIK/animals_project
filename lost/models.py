from django.db import models

from general_data.models import GeneralAnimalModel

# Create your models here.


class LostAnimal(GeneralAnimalModel):  # модель животного-потеряшки

    absolute_url = 'sent_to_moderate'

    place = models.CharField(max_length=200, verbose_name='Где пропал(а)')
    time = models.CharField(max_length=200, verbose_name='Когда пропал(а)')
    special_signs = models.CharField(max_length=200, verbose_name='Особые приметы', blank=True)

    class Meta:
        verbose_name = 'Потерянное животное'
        verbose_name_plural = 'Потерянные животные'

