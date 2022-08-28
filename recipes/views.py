from django.shortcuts import render
from utils.recipes.factory import get_fake


def home(request):
    return render(request, "recipes/pages/home.html", context={
        'recipes': [get_fake() for _ in range(6)]
    })


def recipe(request, id):
    return render(
        request, "recipes/pages/recipe-view.html",
        context={'recipe': get_fake()}
        )
