from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('signup/', views.UserCreationView.as_view(), name='signup')
]
