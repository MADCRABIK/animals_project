from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from os import remove

from django.contrib.auth.models import User

from general_data.models import AnimalType, GeneralAnimalModel


# Create test for your models here


class AnimalTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        AnimalType.objects.create(name='test_name')

    def test_content(self):  # testing object's content
        animal_type = AnimalType.objects.get(id=1)
        self.assertEquals(animal_type.name, 'test_name')

    def test_name_label(self):  # testing verbose name for field 'name'
        animal_type = AnimalType.objects.get(id=1)
        field_label = animal_type._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_name_max_length(self):  # testing max length for field 'name'
        animal_type = AnimalType.objects.get(id=1)
        max_length = animal_type._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_str(self):  # testing object str method
        animal_type = AnimalType.objects.get(id=1)
        expected_object_name = animal_type.name
        self.assertEquals(expected_object_name, str(animal_type))


class GeneralAnimalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create(username='test_user', password='TestPassword123')
        animal_type = AnimalType.objects.create(name='test_name')

        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        GeneralAnimalModel.objects.create(author=test_user,
                                          type=animal_type,
                                          name='test_name',
                                          description='test_description',
                                          photo=test_photo,
                                          phone_number='+79123425939')

    def test_content(self):
        obj = GeneralAnimalModel.objects.get(id=1)
        user = User.objects.get(id=1)
        animal_type = AnimalType.objects.get(id=1)

        self.assertEquals(obj.author, user)
        self.assertEquals(obj.type, animal_type)
        self.assertEquals(obj.name, 'test_name')
        self.assertEquals(obj.description, 'test_description')

        with open('media/test/images/test_image.png', 'rb') as test_picture:
            test_picture = ImageFieldFile(test_picture, ImageField(), 'test_image.png')
            obj.photo = test_picture
            obj.save()
            self.assertEquals(obj.photo, test_picture)
            remove('media/photos/test_image.png')





