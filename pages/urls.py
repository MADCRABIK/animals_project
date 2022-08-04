from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('sent_to_moderate/', views.sent_to_moderate, name='sent_to_moderate'),
]