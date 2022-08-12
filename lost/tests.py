from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from django.urls import reverse
from os import remove

# МОДЕЛИ ДЛЯ ТЕСТИРОВАНИЯ
from django.contrib.auth.models import User
from .models import LostAnimal
from general_data.models import AnimalType


# Create your tests here.


# ТЕСТИРОВАНИЕ МОДЕЛЕЙ


class LostAnimalTest(TestCase):

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
        LostAnimal.objects.create(author=test_user,
                                  type=animal_type,
                                  name='test_name',
                                  description='test_description',
                                  photo=test_photo,
                                  phone_number='+79123425939',
                                  place='test_place',
                                  time='test_time',
                                  special_signs='test_special_signs')

    def test_content(self):  # тестируем содержимое полей
        obj = LostAnimal.objects.get(id=1)
        user = User.objects.get(id=1)
        animal_type = AnimalType.objects.get(id=1)

        self.assertEquals(obj.author, user)
        self.assertEquals(obj.type, animal_type)
        self.assertEquals(obj.name, 'test_name')
        self.assertEquals(obj.description, 'test_description')
        self.assertEquals(obj.phone_number, '+79123425939')
        self.assertEquals(obj.place, 'test_place')
        self.assertEquals(obj.time, 'test_time')
        self.assertEquals(obj.special_signs, 'test_special_signs')

        # Здесь используем классы ImageFieldFile ImageField предоставленные Django,
        # чтобы изменить тип объекта(файла изображения) на ImageFileField для корректного сравнения
        with open('media/test/images/test_image.png') as test_picture:
            test_picture = ImageFieldFile(test_picture, ImageField(), 'test_image.png')
            obj.photo = test_picture
            obj.save()
            self.assertEquals(obj.photo, test_picture)

            # После создания объекта в папке media сохраняется тестовая картинка из его поля photo
            # Чтобы не засорять хранилище после завершения теста эта картинка удаляется
            remove('media/photos/test_image.png')

    def test_labels(self):  # тестируем verbose_name всех полей
        obj = LostAnimal.objects.get(id=1)

        author_label = obj._meta.get_field('author').verbose_name
        type_label = obj._meta.get_field('type').verbose_name
        name_label = obj._meta.get_field('name').verbose_name
        description_label = obj._meta.get_field('description').verbose_name
        phone_number_label = obj._meta.get_field('phone_number').verbose_name
        place_label = obj._meta.get_field('place').verbose_name
        time_label = obj._meta.get_field('time').verbose_name
        special_signs_label = obj._meta.get_field('special_signs').verbose_name
        photo_label = obj._meta.get_field('photo').verbose_name

        self.assertEquals(author_label, 'Автор')
        self.assertEquals(type_label, 'Тип животного')
        self.assertEquals(name_label, 'Кличка')
        self.assertEquals(description_label, 'Описание')
        self.assertEquals(phone_number_label, 'Телефон для связи')
        self.assertEquals(place_label, 'Где пропал(а)')
        self.assertEquals(time_label, 'Когда пропал(а)')
        self.assertEquals(special_signs_label, 'Особые приметы')
        self.assertEquals(photo_label, 'Фото')

    def test_max_length(self):  # тестируем параметр max_length в полях, где он определен
        obj = LostAnimal.objects.get(id=1)

        name_length = obj._meta.get_field('name').max_length
        phone_number_length = obj._meta.get_field('phone_number').max_length
        place_length = obj._meta.get_field('place').max_length
        time_length = obj._meta.get_field('time').max_length
        special_signs_length = obj._meta.get_field('special_signs').max_length

        self.assertEquals(name_length, 200)
        self.assertEquals(phone_number_length, 12)
        self.assertEquals(place_length, 200)
        self.assertEquals(time_length, 200)
        self.assertEquals(special_signs_length, 200)

    def test_object_name_str(self):  # тестируем строковое представление объекта (метод str)
        obj = LostAnimal.objects.get(id=1)
        expected_object_name = obj.name

        self.assertEquals(expected_object_name, str(obj))


# ТЕСТИРОВАНИЕ VIEWS


class LostAnimalListViewTest(TestCase):

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

        for ad in range(2):
            # Создаем объект для дальнейшего тестирования
            LostAnimal.objects.create(author=test_user,
                                      type=animal_type,
                                      name='test_name %s' % ad,
                                      description='test_description %s' % ad,
                                      photo=test_photo,
                                      phone_number='+79123425939',
                                      place='test_place %s' % ad,
                                      time='test_time %s' % ad,
                                      special_signs='test_special_signs %s' % ad,
                                      moderated=True)

            remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        response = self.client.get('/lost/list/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('lost_list'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('lost_list'))
        self.assertTemplateUsed(response, 'lost/lost_list.html')

    def test_view_context(self):
        response = self.client.get(reverse('lost_list'))
        object_list = list(LostAnimal.objects.filter(moderated=True))
        self.assertQuerysetEqual(response.context['lostanimal_list'].order_by('published'), object_list)


class LostAnimalCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):  # СОЗДАЕМ ЮЗЕРА ДЛЯ ДОСТУПА КО VIEW
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

    def test_view_url_exists(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='test_username', password='test_password')
        response = self.client.get('/lost/create/')
        self.assertEquals(response.status_code, 200)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get('/lost/create/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_create'))
        self.assertEquals(response.status_code, 200)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(reverse('lost_create'))
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_create'))
        self.assertTemplateUsed(response, 'lost/lost_create.html')

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.logout()
        response = self.client.get(reverse('lost_create'))
        self.assertTemplateNotUsed(response, 'lost/lost_create.html')


class LostAnimalDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # СОЗДАЕМ ЮЗЕРА
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

        # Создаем animal_type чтобы передать его в поле "type" объекта
        animal_type = AnimalType.objects.create(name='test_name')

        # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        # Создаем объект для дальнейшего тестирования
        LostAnimal.objects.create(author=test_user,
                                  type=animal_type,
                                  name='test_name',
                                  description='test_description',
                                  photo=test_photo,
                                  phone_number='+79123425939',
                                  place='test_place',
                                  time='test_time',
                                  special_signs='test_special_signs',
                                  moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        obj = LostAnimal.objects.get(id=1)

        response = self.client.get(f'/lost/detail/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        obj = LostAnimal.objects.get(id=1)

        response = self.client.get(reverse('lost_detail', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        obj = LostAnimal.objects.get(id=1)

        response = self.client.get(reverse('lost_detail', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'lost/lost_detail.html')

    def test_view_context(self):
        obj = LostAnimal.objects.get(id=1)
        response = self.client.get(reverse('lost_detail', kwargs={'pk': obj.pk}))
        self.assertEquals(response.context['animal'], obj)


class LostAnimalUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # СОЗДАЕМ ЮЗЕРА ДЛЯ ДОСТУПА КО VIEW
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

        wrong_test_user = User.objects.create(username='wrong_user')
        wrong_test_user.set_password('wrong_password')
        wrong_test_user.save()

        super_user = User.objects.create(username='super_user', is_superuser=True)
        super_user.set_password('super_user_password')
        super_user.save()

        # Создаем animal_type чтобы передать его в поле "type" объекта
        animal_type = AnimalType.objects.create(name='test_name')

        # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        # Создаем объект для дальнейшего тестирования
        LostAnimal.objects.create(author=test_user,
                                  type=animal_type,
                                  name='test_name',
                                  description='test_description',
                                  photo=test_photo,
                                  phone_number='+79123425939',
                                  place='test_place',
                                  time='test_time',
                                  special_signs='test_special_signs',
                                  moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(f'/lost/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(f'/lost/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(f'/lost/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(f'/lost/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

    def test_view_url_access_by_name(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

    def test_view_uses_correct_template(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'lost/lost_edit.html')

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'lost/lost_edit.html')

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateNotUsed(response, 'lost/lost_edit.html')

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.logout()
        response = self.client.get(reverse('lost_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateNotUsed(response, 'lost/lost_edit.html')


class LostAnimalDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # СОЗДАЕМ ЮЗЕРА ДЛЯ ДОСТУПА КО VIEW
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

        wrong_test_user = User.objects.create(username='wrong_user')
        wrong_test_user.set_password('wrong_password')
        wrong_test_user.save()

        super_user = User.objects.create(username='super_user', is_superuser=True)
        super_user.set_password('super_user_password')
        super_user.save()

        # Создаем animal_type чтобы передать его в поле "type" объекта
        animal_type = AnimalType.objects.create(name='test_name')

        # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        # создаем объект для дальнейшего тестирования
        LostAnimal.objects.create(author=test_user,
                                  type=animal_type,
                                  name='test_name',
                                  description='test_description',
                                  photo=test_photo,
                                  phone_number='+79123425939',
                                  place='test_place',
                                  time='test_time',
                                  special_signs='test_special_signs',
                                  moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists_author(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(f'/lost/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_exists_superuser(self):
        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(f'/lost/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_exists_wrong_user(self):
        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(f'/lost/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

    def test_view_url_exists_logout(self):
        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = LostAnimal.objects.get(id=1)
        self.client.logout()
        response = self.client.get(f'/lost/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 404)


    def test_view_url_access_by_name_author(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name_superuser(self):
        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('lost_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name_wrong_user(self):
        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = LostAnimal.objects.get(id=1)
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('lost_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

    def test_view_url_access_by_name_logout(self):
        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = LostAnimal.objects.get(id=1)
        self.client.logout()
        response = self.client.get(reverse('lost_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

