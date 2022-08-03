from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('to_moderate/', views.to_moderate, name='to_moderate'),
    path('publish_lost/<int:pk>', views.publish_lost, name='publish_lost'),
    path('publish_good_hands/<int:pk>', views.publish_good_hands, name='publish_good_hands'),
    path('reject_lost/<int:pk>', views.reject_lost, name='reject_lost'),
    path('reject_good_hands/<int:pk>', views.reject_good_hands, name='reject_good_hands'),
]
