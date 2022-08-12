from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile, ImageField
from os import remove

from django.contrib.auth.models import User

from general_data.models import AnimalType
from lost.models import LostAnimal
from good_hands.models import AnimalToGoodHands

# Create your tests here.


class ToModerateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем юзера для передачи его в поле "author" объекта
        test_user = User.objects.create(username='test_user')
        test_user.set_password('test_password')
        test_user.save()

        # Создаем суперюзера для доступа к разделу модерации
        superuser = User.objects.create(username='superuser', is_superuser=True)
        superuser.set_password('super_user_password')
        superuser.save()

        # Создаем animal_type чтобы передать его в поле "type" объекта
        animal_type = AnimalType.objects.create(name='test_name')

        # Создаем test_photo с помощью специального класса для передачи его в поле 'photo' объекта
        test_photo = SimpleUploadedFile(name='test_image.png',
                                        content=open('media/test/images/test_image.png', 'rb').read(),
                                        content_type='image/png')

        for ad in range(2):
            # Создаем объект модели LostAnimal для дальнейшего тестирования
            LostAnimal.objects.create(author=test_user,
                                      type=animal_type,
                                      name='test_name %s' % ad,
                                      description='test_description %s' % ad,
                                      photo=test_photo,
                                      phone_number='+79123425939',
                                      place='test_place %s' % ad,
                                      time='test_time %s' % ad,
                                      special_signs='test_special_signs %s' % ad,
                                      moderated=False)

            # Создаем объект модели AnimalToGoodHands для дальнейшего тестирования
            AnimalToGoodHands.objects.create(author=test_user,
                                             type=animal_type,
                                             name='test_name %s' % ad,
                                             description='test_description %s' % ad,
                                             photo=test_photo,
                                             phone_number='+79123425939',
                                             moderated=False)

            remove('media/photos/test_image.png')

    def test_view_url_exists(self):
        # проверяем отсутствие доступа если пользователь не аутентифицирован
        response = self.client.get('/moderation/to_moderate/')
        self.assertEquals(response.status_code, 302)

        # проверяем отсутствие доступа если пользователь не суперюзер
        self.client.login(username='test_user', password='test_password')
        response = self.client.get('/moderation/to_moderate/')
        self.assertEquals(response.status_code, 302)

        # проверяем наличие доступа если пользователь суперюзер
        self.client.login(username='superuser', password='super_user_password')
        response = self.client.get('/moderation/to_moderate/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        # проверяем отсутствие доступа если пользователь не аутентифицирован
        response = self.client.get(reverse('to_moderate'))
        self.assertEquals(response.status_code, 302)

        # проверяем отсутствие доступа если пользователь не суперюзер
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('to_moderate'))
        self.assertEquals(response.status_code, 302)

        # проверяем наличие доступа если пользователь суперюзер
        self.client.login(username='superuser', password='super_user_password')
        response = self.client.get(reverse('to_moderate'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # проверяем отсутствие доступа к шаблону если пользователь не аутентифицирован
        response = self.client.get(reverse('to_moderate'))
        self.assertTemplateNotUsed(response, 'moderation/moderate_list.html')

        # проверяем отсутствие доступа к шаблону если пользователь не суперюзер
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('to_moderate'))
        self.assertTemplateNotUsed(response, 'moderation/moderate_list.html')

        # проверяем наличие доступа к шаблону если пользователь суперюзер
        self.client.login(username='superuser', password='super_user_password')
        response = self.client.get(reverse('to_moderate'))
        self.assertTemplateUsed(response, 'moderation/moderate_list.html')

    def test_view_context(self):
        response = self.client.get(reverse('lost_list'))
        object_list = list(LostAnimal.objects.filter(moderated=True))
        self.assertQuerysetEqual(response.context['lostanimal_list'].order_by('published'), object_list)
        self.assertQuerysetEqual(response.context['lostanimal_list'].order_by('published'), object_list)