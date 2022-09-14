from django.http import Http404
from django.shortcuts import (HttpResponse, get_list_or_404, get_object_or_404,
                              render)

from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    return HttpResponse(
        content=render(
            request, "recipes/pages/home.html", context={"recipes": recipes}
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

    # if not recipes:
    #     # return HttpResponse(content="Not Found", status=404)
    #     raise Http404("Nada Aqui")

    return render(
        request,
        "recipes/pages/category.html",
        context={"recipes": recipes,
                 "title": f"{recipes[0].category.name} | Category"},
    )


def search(request):
    term_search = request.GET.get('search', '').strip()

    if not term_search:
        raise Http404()

    return render(
        request,
        "recipes/pages/search.html",
        context={
            'page_title': f'Search for "{term_search}" |',
            'term_search': term_search
        }
    )
