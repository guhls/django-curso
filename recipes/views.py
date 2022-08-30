from django.shortcuts import render
from utils.recipes.factory import get_fake
from .models import Recipe
from django.http import HttpResponse, Http404


def home(request):
    return render(request, "recipes/pages/home.html", context={
        'recipes': Recipe.objects.filter(is_published=True)
    })


def recipe(request, id):
    return render(
        request, "recipes/pages/recipe-view.html",
        context={
            'recipe': get_fake(),
            'is_detail': True,
            }
        )


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True
        )

    if not recipes:
        # return HttpResponse(content="Not Found", status=404)
        raise Http404("Nada Aqui")

    return render(request, "recipes/pages/category.html", context={
        "recipes": recipes,
        "title": f'{recipes.first().category.name} | Category'
    })
