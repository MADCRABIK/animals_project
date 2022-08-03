from django.contrib import admin

from .models import AnimalType

# Register your models here.


class AnimalTypeAdmin(admin.ModelAdmin):  # настройка представления модели AnimalType в админке
    list_display = ('name', )  # отображаемые поля

    list_display_links = ('name', )  # поля-ссылки

    search_fields = ('name', )  # поля по которым производится поиск


admin.site.register(AnimalType)  # регистрируем модель AnimalType в админке
