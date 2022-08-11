from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('list/', views.LostAnimalListView.as_view(), name='lost_list'),
    path('create/', views.LostAnimalCreateView.as_view(), name='lost_create'),
    path('detail/<int:pk>/', views.LostAnimalDetailView.as_view(), name='lost_detail'),
    path('edit/<int:pk>/', views.LostAnimalUpdateView.as_view(), name='lost_edit'),
    path('delete/<int:pk>/', views.lost_animal_delete, name='lost_delete'),
]