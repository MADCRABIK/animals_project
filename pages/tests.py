from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your tests here.


class HomePageViewTest(TestCase):

    def test_view_url_exists(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'pages/home.html')


class AboutPageViewTest(TestCase):

    def test_view_url_exists(self):
        response = self.client.get('/about/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'pages/about.html')


class SentToModeratePageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(username='test_username')
        test_user.set_password('test_password')
        test_user.save()

    def test_view_url_exists(self):
        # проверяем, что при попытке перейти напрямую по URL нас редиректит
        response = self.client.get('/sent_to_moderate/')
        self.assertEquals(response.status_code, 302)

        # проверяем, что если мы переходим на URL с URL'а 'lost_create', то все работает
        self.client.login(username='test_username', password='test_password')
        response = self.client.get('/lost/create/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/sent_to_moderate/', follow=True)
        self.assertEquals(response.status_code, 200)

        # проверяем через имя URL'а что если мы переходим на него с URL'а 'good_hands_create', то все работает
        response = self.client.get('/good_hands/create/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/sent_to_moderate/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_view_url_access_by_name(self):
        # проверяем через имя URL'а, что при попытке перейти напрямую по URL нас редиректит
        response = self.client.get(reverse('sent_to_moderate'))
        self.assertEquals(response.status_code, 302)

        # проверяем через имя URL'а что если мы переходим на него с URL'а 'lost_create', то все работает
        self.client.login(username='test_username', password='test_password')
        response = self.client.get(reverse('lost_create'))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('sent_to_moderate'), follow=True)
        self.assertEquals(response.status_code, 200)

        # проверяем через имя URL'а что если мы переходим на него с URL'а 'good_hands_create', то все работает
        response = self.client.get(reverse('good_hands_create'))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('sent_to_moderate'), follow=True)
        self.assertEquals(response.status_code, 200)







