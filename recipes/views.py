# from django.shortcuts import render
from django.http import HttpResponse


def my_view(request):
    return HttpResponse('Ola Mundo!!')


def home(response):
    return HttpResponse("/home na urls.py em recipes")
