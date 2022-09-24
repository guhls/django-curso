import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import (HttpResponse, get_list_or_404, get_object_or_404,
                              render)
from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 9))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    recipes_obj, range_pages = make_pagination(request, recipes, PER_PAGE, 4)

    return HttpResponse(
        content=render(
            request,
            "recipes/pages/home.html",
            context={
                "recipes": recipes_obj,
                "range_pages": range_pages,
            }
        ),
        # status=200
    )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        "recipes/pages/recipe-view.html",
        context={
            "recipe": recipe,
            "is_detail": True,
        },
    )


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    recipes_obj, range_pages = make_pagination(request, recipes, PER_PAGE, 4)

    # if not recipes:
    #     # return HttpResponse(content="Not Found", status=404)
    #     raise Http404("Nada Aqui")

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "recipes": recipes_obj,
            "title": f"{recipes[0].category.name} | Category",
            "range_pages": range_pages,
        },
    )


def search(request):
    term_search = request.GET.get('search', '').strip()

    if not term_search:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=term_search) |
            Q(description__icontains=term_search)
        ),
        is_published=True,
    ).order_by('-id')

    recipes_obj, range_pages = make_pagination(request, recipes, PER_PAGE, 4)

    return render(
        request,
        "recipes/pages/search.html",
        context={
            'recipes': recipes_obj,
            'page_title': f'Search for "{term_search}" |',
            'term_search': term_search,
            'range_pages': range_pages,
            'additional_query': f'&search={term_search}'
        }
    )
