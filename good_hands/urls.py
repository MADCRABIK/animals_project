from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('list/', views.GoodHandsListView.as_view(), name='good_hands_list'),
    path('create/', views.GoodHandsCreateView.as_view(), name='good_hands_create'),
    path('detail/<int:pk>/', views.GoodHandsDetailView.as_view(), name='good_hands_detail'),
    path('edit/<int:pk>/', views.GoodHandsUpdateView.as_view(), name='good_hands_edit'),
    path('delete/<int:pk>/', views.good_hands_delete, name='good_hands_delete'),
]