import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from loginsys.froms import RegisterForm, LoginForm


@csrf_protect
def index(request):
    if not request.user.is_authenticated:
        form_register = RegisterForm()
        form_auth = LoginForm()
        context = {'form_register': form_register, 'form_auth': form_auth}
        context.update(csrf(request))
        return render(request, 'loginsys/index.html', context)
    else:
        return redirect('lessons:lesson_list')


@csrf_protect
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('lessons:lesson_list')
    else:
        form_auth = LoginForm()
        return render(request, 'loginsys/index.html', {'form_register': form, 'form_auth': form_auth})


@csrf_protect
def auth(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print("text")
        user = form.get_user()
        login(request, user)
        return redirect('lessons:lesson_list')
    else:
        form_register = RegisterForm()
        return render(request, 'loginsys/index.html', {'form_register': form_register, 'form_auth': form})


@csrf_protect
def profilelogout(request):
    logout(request)
    return redirect('/')


def contacts(request):
    return render(request, 'loginsys/contacts.html')


def about(request):
    return render(request, 'loginsys/about.html')
