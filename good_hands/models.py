from general_data.models import GeneralAnimalModel

# Create your models here.


class AnimalToGoodHands(GeneralAnimalModel):  # модель животного-потеряшки

    absolute_url = 'sent_to_moderate'

    class Meta:
        verbose_name = 'Животное в добрые руки'
        verbose_name_plural = 'Животные в добрые руки'
