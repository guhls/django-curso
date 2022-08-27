from django.shortcuts import render


def home(request):
    return render(request, "recipes/pages/home.html", context={
        "Nome": "Gustavo",
        "Idade": 21,
        "Title": "Recipes"
    })
