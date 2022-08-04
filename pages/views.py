from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.


def home_page(request):  # домашняя страница сайта
    return render(request, 'pages/home.html')


def about_page(request):  # страница "о сайте"
    return render(request, 'pages/about.html')


def sent_to_moderate(request):  # страница "отправлено на модерацию"
    return render(request, 'pages/sent_to_moderate.html')
