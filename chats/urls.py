from django.urls import path

from . import views

# Create your URLS here


urlpatterns = [
    path('', views.dialog_list_view, name='chats'),
    path('<int:pk>/', views.dialog_detail_view, name='chat_detail'),
    path('get_dialog/<int:author_id>/', views.get_dialog, name='get_dialog'),
]

