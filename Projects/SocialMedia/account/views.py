from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
import datetime

from .forms import RegistrationForm, LoginForm
from .models import Account

@require_http_methods(["GET", "POST"])
def signin(request, *args, **kwargs):

    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
       
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)

                next = kwargs.get('next')

                if next:
                    return redirect(next)

                return redirect('home')

    return render(request, 'account/login.html', {'form':form})


@require_http_methods(["GET", "POST"])
def register(request, *args, **kwargs):

    if request.user.is_authenticated:
        return redirect('home')

    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
       
        if form.is_valid():
            form.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])

            if user is not None:
                login(request, user)

                next = kwargs.get('next')

                if next:
                    return redirect(next)

                return redirect('home')

    return render(request, 'account/register.html', {'form':form})
    

@require_http_methods(["POST"])
@login_required
def signout(request):
    
    logout(request)
    return redirect('login')
    