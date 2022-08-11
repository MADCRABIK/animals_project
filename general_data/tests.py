from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from os import remove

from django.contrib.auth.models import User

from .models import AnimalType, GeneralAnimalModel


# Test your app here


class AnimalTypeTest(TestCase):  # ТЕСТИРУЕМ МОДЕЛЬ AnimalType

    @classmethod
    def setUpTestData(cls):
        # Создаем объект для дальнейшего тестирования
        AnimalType.objects.create(name='test_name')

    def test_content(self):  # тестируем содержимое полей
        animal_type = AnimalType.objects.get(id=1)
        self.assertEquals(animal_type.name, 'test_name')

    def test_name_label(self):  # тестируем параметр verbose_name для поля name
        animal_type = AnimalType.objects.get(id=1)
        field_label = animal_type._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_name_max_length(self):  # тестируем параметр max_length для поля name
        animal_type = AnimalType.objects.get(id=1)
        max_length = animal_type._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_str(self):  # тестируем строковое представление объекта (метод str)
        animal_type = AnimalType.objects.get(id=1)
        expected_object_name = animal_type.name
        self.assertEquals(expected_object_name, str(animal_type))
