from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


def register(request):
    request.session['number'] = request.session.get('number', 0)
    request.session['number'] += 1

    form_data = request.session.get('form_data', None)
    form = RegisterForm(form_data)

    return render(request, 'authors/pages/register.html', context={
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(request, 'User Created')

        del (request.session['form_data'])

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )

        if authenticate_user:
            login(request, authenticate_user)
            messages.success(request, 'You are Log in')
        else:
            messages.error(request, 'Invalid Login')
    else:
        messages.error(request, 'Username or Password invalid')

    return redirect(reverse('authors:login'))
