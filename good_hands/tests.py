from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from os import remove

from django.contrib.auth.models import User

# МОДЕЛИ ДЛЯ ТЕСТИРОВАНИЯ
from .models import AnimalToGoodHands
from general_data.models import AnimalType


# Create your tests here.

# ТЕСТИРОВАНИЕ МОДЕЛЕЙ


class AnimalToGoodHandsTest(TestCase):

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
        AnimalToGoodHands.objects.create(author=test_user,
                                         type=animal_type,
                                         name='test_name',
                                         description='test_description',
                                         photo=test_photo,
                                         phone_number='+79123425939')

    def test_content(self):  # тестируем содержимое полей
        obj = AnimalToGoodHands.objects.get(id=1)
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
        obj = AnimalToGoodHands.objects.get(id=1)

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
        obj = AnimalToGoodHands.objects.get(id=1)

        name_length = obj._meta.get_field('name').max_length
        phone_number_length = obj._meta.get_field('phone_number').max_length

        self.assertEquals(name_length, 200)
        self.assertEquals(phone_number_length, 12)

    def test_object_name_str(self):  # тестируем строковое представление объекта (метод str)
        obj = AnimalToGoodHands.objects.get(id=1)
        expected_object_name = obj.name

        self.assertEquals(expected_object_name, str(obj))


# ТЕСТИРОВАНИЕ VIEWS

class GoodHandsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_ads = 5
        for ad in range(number_of_ads):
            # Создаем юзера для передачи его в поле "author" объекта
            test_user = User.objects.create(username='test_user %s' % ad, password='TestPassword123')
            # Создаем animal_type чтобы передать его в поле "type" объекта
            animal_type = AnimalType.objects.create(name='test_name %s' % ad)

            # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
            test_photo = SimpleUploadedFile(name='test_image.png',
                                            content=open('media/test/images/test_image.png', 'rb').read(),
                                            content_type='image/png')

            # Создаем объект для дальнейшего тестирования
            AnimalToGoodHands.objects.create(author=test_user,
                                             type=animal_type,
                                             name='test_name %s' % ad,
                                             description='test_description %s' % ad,
                                             photo=test_photo,
                                             phone_number='+79123425939',
                                             moderated=True)

            remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        response = self.client.get('/good_hands/list/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('good_hands_list'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('good_hands_list'))
        self.assertTemplateUsed(response, 'good_hands/good_hands_list.html')

    def test_view_context(self):
        response = self.client.get(reverse('good_hands_list'))
        object_list = list(AnimalToGoodHands.objects.filter(moderated=True))
        self.assertQuerysetEqual(response.context['animaltogoodhands_list'].order_by('published'), object_list)


class GoodHandsCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):  # СОЗДАЕМ ЮЗЕРА ДЛЯ ДОСТУПА КО VIEW
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

    def test_view_url_exists(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='test_username', password='test_password')
        response = self.client.get('/good_hands/create/')
        self.assertEquals(response.status_code, 200)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get('/good_hands/create/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('good_hands_create'))
        self.assertEquals(response.status_code, 200)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(reverse('good_hands_create'))
        self.assertEquals(response.status_code, 302)

    def test_view_uses_correct_template(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('good_hands_create'))
        self.assertTemplateUsed(response, 'good_hands/good_hands_create.html')

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.logout()
        response = self.client.get(reverse('good_hands_create'))
        self.assertTemplateNotUsed(response, 'good_hands/good_hands_create.html')


class GoodHandsDetailViewTest(TestCase):

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
        AnimalToGoodHands.objects.create(author=test_user,
                                         type=animal_type,
                                         name='test_name',
                                         description='test_description',
                                         photo=test_photo,
                                         phone_number='+79123425939',
                                         moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        obj = AnimalToGoodHands.objects.get(id=1)

        response = self.client.get(f'/good_hands/detail/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        obj = AnimalToGoodHands.objects.get(id=1)

        response = self.client.get(reverse('good_hands_detail', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        obj = AnimalToGoodHands.objects.get(id=1)

        response = self.client.get(reverse('good_hands_detail', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'good_hands/good_hands_detail.html')

    def test_view_context(self):
        obj = AnimalToGoodHands.objects.get(id=1)
        response = self.client.get(reverse('good_hands_detail', kwargs={'pk': obj.pk}))
        self.assertEquals(response.context['animal'], obj)


class GoodHandsUpdateViewTest(TestCase):

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
        AnimalToGoodHands.objects.create(author=test_user,
                                         type=animal_type,
                                         name='test_name',
                                         description='test_description',
                                         photo=test_photo,
                                         phone_number='+79123425939',
                                         moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(f'/good_hands/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(f'/good_hands/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(f'/good_hands/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(f'/good_hands/edit/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

    def test_view_url_access_by_name(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 200)

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        self.client.logout()
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

    def test_view_uses_correct_template(self):
        # ЛОГИНИМ ЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'good_hands/good_hands_edit.html')

        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ИСПОЛЬЗУЕМЫЙ ШАБЛОН
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateUsed(response, 'good_hands/good_hands_edit.html')

        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateNotUsed(response, 'good_hands/good_hands_edit.html')

        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА К ШАБЛОНУ НЕТ
        self.client.logout()
        response = self.client.get(reverse('good_hands_edit', kwargs={'pk': obj.pk}))
        self.assertTemplateNotUsed(response, 'good_hands/good_hands_edit.html')


class GoodHandslDeleteViewTest(TestCase):

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
        AnimalToGoodHands.objects.create(author=test_user,
                                         type=animal_type,
                                         name='test_name',
                                         description='test_description',
                                         photo=test_photo,
                                         phone_number='+79123425939',
                                         moderated=True, )

        remove('media/photos/test_image.png')

    def test_view_url_exists_author(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(f'/good_hands/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_exists_superuser(self):
        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(f'/good_hands/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_exists_wrong_user(self):
        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(f'/good_hands/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 404)

    def test_view_url_exists_logout(self):
        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.logout()
        response = self.client.get(f'/good_hands/delete/{obj.pk}/')
        self.assertEquals(response.status_code, 404)


    def test_view_url_access_by_name_author(self):
        # ЛОГИНИМ ЮЗЕРА(АВТОРА) И ПРОВЕРЯЕМ ДОСТУП К СТРАНИЦЕ ПО ИМЕНИ URL
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('good_hands_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name_superuser(self):
        # ЛОГИНИМ СУПЕРЮЗЕРА И ПРОВЕРЯЕМ ЧТО ДОСТУП К СТРАНИЦЕ ПО URL АДРЕСУ ЕСТЬ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='super_user', password='super_user_password')
        response = self.client.get(reverse('good_hands_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 302)

    def test_view_url_access_by_name_wrong_user(self):
        # ЛОГИНИМ ЛЕВОГО ЮЗЕРА (НЕ АВТОРА) И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.login(username='wrong_user', password='wrong_password')
        response = self.client.get(reverse('good_hands_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

    def test_view_url_access_by_name_logout(self):
        # ДЕЛАЕМ ЛОГАУТ И УБЕЖДАЕМСЯ ЧТО ДОСТУПА НЕТ
        obj = AnimalToGoodHands.objects.get(id=1)
        self.client.logout()
        response = self.client.get(reverse('good_hands_delete', kwargs={'pk': obj.pk}))
        self.assertEquals(response.status_code, 404)

