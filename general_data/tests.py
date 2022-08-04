from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from os import remove

from django.contrib.auth.models import User

from general_data.models import AnimalType, GeneralAnimalModel


# Create test for your models here


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


class GeneralAnimalModelTest(TestCase):   # ТЕСТИРУЕМ МОДЕЛЬ GeneralAnimalModel

    @classmethod
    def setUpTestData(cls):

        # Создаем юзера для передачи его в поле "author" объекта
        test_user = User.objects.create(username='test_user', password='TestPassword123')
        # Создаем animal_type чтобы передать его в поле "type" объекта
        animal_type = AnimalType.objects.create(name='test_name')
        # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        # Создаем объект для дальнейшего тестирования
        GeneralAnimalModel.objects.create(author=test_user,
                                          type=animal_type,
                                          name='test_name',
                                          description='test_description',
                                          photo=test_photo,
                                          phone_number='+79123425939')

    def test_content(self):  # тестируем содержимое полей
        obj = GeneralAnimalModel.objects.get(id=1)
        user = User.objects.get(id=1)
        animal_type = AnimalType.objects.get(id=1)

        self.assertEquals(obj.author, user)
        self.assertEquals(obj.type, animal_type)
        self.assertEquals(obj.name, 'test_name')
        self.assertEquals(obj.description, 'test_description')

        # Здесь используем классы ImageFieldFile ImageField предоставленные Django,
        # чтобы изменить тип объекта(файла изображения) на ImageFileField для корректного сравнения
        with open('media/test/images/test_image.png', 'rb') as test_picture:
            test_picture = ImageFieldFile(test_picture, ImageField(), 'test_image.png')
            obj.photo = test_picture
            obj.save()
            self.assertEquals(obj.photo, test_picture)

            # После создания объекта в папке media сохраняется тестовая картинка из его поля photo
            # Чтобы не засорять хранилище после завершения теста эта картинка удаляется
            remove('media/photos/test_image.png')

    def test_labels(self):  # тестируем verbose_name всех полей
        obj = GeneralAnimalModel.objects.get(id=1)

        author_label = obj._meta.get_field('author').verbose_name
        type_label = obj._meta.get_field('type').verbose_name
        name_label = obj._meta.get_field('name').verbose_name
        description_label = obj._meta.get_field('description').verbose_name
        photo_label = obj._meta.get_field('photo').verbose_name
        phone_number_label = obj._meta.get_field('phone_number').verbose_name

        self.assertEquals(author_label, 'Автор')
        self.assertEquals(type_label, 'Тип животного')
        self.assertEquals(name_label, 'Кличка')
        self.assertEquals(description_label, 'Описание')
        self.assertEquals(photo_label, 'Фото')
        self.assertEquals(phone_number_label, 'Телефон для связи')

    def test_max_length(self):  # тестируем параметр max_length в полях, где он определен
        obj = GeneralAnimalModel.objects.get(id=1)

        name_length = obj._meta.get_field('name').max_length
        phone_number_length = obj._meta.get_field('phone_number').max_length

        self.assertEquals(name_length, 200)
        self.assertEquals(phone_number_length, 12)

    def test_object_name_str(self):  # тестируем строковое представление объекта (метод str)
        obj = GeneralAnimalModel.objects.get(id=1)
        expected_object_name = obj.name

        self.assertEquals(expected_object_name, str(obj))
