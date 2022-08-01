from django.contrib import admin

from .models import LostAnimal, AnimalType

# Register your models here.


class LostAnimalAdmin(admin.ModelAdmin):  # настройка представления модели LostAnimal в админке
    list_display = ('name',  # отображаемые поля
                    'photo',
                    'place',
                    'time',
                    'special_signs',
                    'description',
                    'phone_number',
                    'published',
                    )

    list_display_links = ('name', 'photo', 'description', )  # поля-ссылки

    search_fields = ('name',  # поля по которым производится поиск
                     'place',
                     'time',
                     'special_signs',
                     'description',
                     'phone_number',
                     )


admin.site.register(LostAnimal, LostAnimalAdmin)  # регистрируем модель LostAnimal в админке
admin.site.register(AnimalType)  # регистрируем модель AnimalType в админке
