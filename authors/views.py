from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    request.session['number'] = request.session.get('number', 0)
    request.session['number'] += 1

    form_data = request.session.get('form_data', None)
    form = RegisterForm(form_data)

    return render(request, 'authors/pages/register.html', context={
        'form': form
    })


def create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['form_data'] = POST
    form = RegisterForm(POST)

    return redirect('authors:register')
