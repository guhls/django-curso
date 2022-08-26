from django.shortcuts import render
from django.http import HttpResponse


def my_view(request):
    return render(request, 'global/home.html')


def home(response):
    return HttpResponse("/home na urls.py em recipes")
