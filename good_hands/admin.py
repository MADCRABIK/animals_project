from django.contrib import admin

from .models import AnimalToGoodHands

# Register your models here.


class AnimalToGoodHandsAdmin(admin.ModelAdmin):  # настройка представления модели AnimalToGoodHands в админке
    list_display = ('author',  # отображаемые поля
                    'name',
                    'photo',
                    'description',
                    'phone_number',
                    'published',
                    'moderated',
                    )

    list_display_links = ('author', 'name', 'photo', 'description', )  # поля-ссылки

    search_fields = ('author',  # поля по которым производится поиск
                     'name',
                     'description',
                     'phone_number',
                     )


admin.site.register(AnimalToGoodHands, AnimalToGoodHandsAdmin)  # регистрируем модель AnimalToGoodHands в админке

