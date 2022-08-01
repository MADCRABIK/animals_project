from django.shortcuts import render

# Create your views here.


def home_page(request):  # домашняя страница сайта
    return render(request, 'pages/home.html')


def about_page(request):  # страница "о сайте"
    return render(request, 'pages/about.html')
