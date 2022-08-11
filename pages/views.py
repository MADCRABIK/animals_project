from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

# Create your views here.


def home_page(request):  # домашняя страница сайта
    return render(request, 'pages/home.html')


def about_page(request):  # страница "о сайте"
    return render(request, 'pages/about.html')


def sent_to_moderate(request):  # страница "отправлено на модерацию"

    # список разрешенных адресов, которых можно делать редирект на sent_to_moderate
    redirect_urls = ('http://127.0.0.1:8000/lost/create/', 'http://127.0.0.1:8000/good_hands/create/')

    # если адрес с которого выполняется редирект есть в списке
    if request.META.get('HTTP_REFERER') in redirect_urls:
        return render(request, 'pages/sent_to_moderate.html')
    # если его нет в списке делаем редирект на главную
    else:
        return HttpResponseRedirect('/')

