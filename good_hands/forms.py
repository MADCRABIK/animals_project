from django.forms import ModelForm

from .models import AnimalToGoodHands

# Create your forms here


class AnimalToGoodHandsForm(ModelForm):

    class Meta:
        model = AnimalToGoodHands
        fields = ('name',  # поля формы
                  'type',
                  'photo',
                  'description',
                  'phone_number',
                  )
