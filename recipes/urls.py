from django.urls import path
from recipes.views import home, my_view


urlpatterns = [
    path('', my_view),
    path('home/', home),
]
