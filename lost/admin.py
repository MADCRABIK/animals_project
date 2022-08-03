from django.contrib import admin

from .models import LostAnimal

# Register your models here.


class LostAnimalAdmin(admin.ModelAdmin):  # настройка представления модели LostAnimal в админке
    list_display = ('author',  # отображаемые поля
                    'name',
                    'photo',
                    'place',
                    'time',
                    'special_signs',
                    'description',
                    'phone_number',
                    'published',
                    'moderated',
                    )

    list_display_links = ('author', 'name', 'photo', 'description', )  # поля-ссылки

    search_fields = ('author',  # поля по которым производится поиск
                     'name',
                     'place',
                     'time',
                     'special_signs',
                     'description',
                     'phone_number',
                     )


admin.site.register(LostAnimal, LostAnimalAdmin)  # регистрируем модель LostAnimal в админке
