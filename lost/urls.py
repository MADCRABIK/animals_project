from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

# Create your URLS here


urlpatterns = [
    path('lost_list/', views.LostAnimalListView.as_view(), name='lost_list'),
    path('lost_create/', views.LostAnimalCreateView.as_view(), name='lost_create'),
    path('lost_detail/<int:pk>', views.LostAnimalDetailView.as_view(), name='lost_detail'),
    path('lost_edit/<int:pk>', views.LostAnimalUpdateView.as_view(), name='lost_edit'),
    path('lost_delete/<int:pk>', views.lost_animal_delete, name='lost_delete'),
]

# Позволяет показывать файлы (картинки). Почему - не знаю. Надо разобраться потом
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


