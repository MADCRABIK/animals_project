from django.forms import ModelForm

from .models import LostAnimal

# Create your forms here


class LostAnimalForm(ModelForm):  # создаем форму на основе модели LostAnimal

    class Meta:
        model = LostAnimal
        fields = ('name',  # поля формы
                  'photo',
                  'type',
                  'place',
                  'time',
                  'special_signs',
                  'description',
                  'phone_number',
                  )
