import datetime

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from . import forms
from . import models


def sign_in(request):
    """Process the user login request"""
    form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request,
                        f"You are now logged in as {user.username}"
                    )
                    return HttpResponseRedirect(reverse('index'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled"
                    )
            else:
                message.error(
                    request,
                    "The username or password is incorrect"
                )
    return render(
        request,
        'menu/login.html',
        {'form': form, 'login_page': 'active'}
    )


def register(request):
    """Create new user account"""
    form = forms.UserRegisterForm()
    if request.method == 'POST':
        form = forms.UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password1'],
            )
            login(request, user)
            messages.success(
                request,
                "You have successfully created a new acount and are " +
                f"now logged in as {user.username}"
            )
            return HttpResponseRedirect(reverse('index'))
    return render(
        request,
        'menu/register.html',
        {'form': form}
    )


def sign_out(request):
    """Log the user out of the site"""
    logout(request)
    messages.success(request, "You've been logged out. Come back soon!")
    return HttpResponseRedirect(reverse('index'))


def menu_detail(request, pk):
    """Display the detailes of a menu"""
    try:
        menu = models.Menu.objects.prefetch_related(
            'items'
        ).get(pk=pk)
    except models.Menu.DoesNotExist:
        raise Http404
    return render(request,
                  'menu/menu_detail.html',
                  {'menu': menu})


def item_detail(request, pk):
    """Display the details of an item"""
    try:
        item = models.Item.objects.prefetch_related(
            'ingredients'
        ).get(pk=pk)
    except models.Item.DoesNotExist:
        raise Http404
    return render(request,
                  'menu/item_detail.html',
                  {'item': item})


@login_required
def create_menu(request):
    """Create a new menu"""
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(data=request.POST)
        if form.is_valid():
            new_menu = form.save(commit=False)
            new_menu.creator = request.user
            new_menu.season = '{} {}'.format(form.cleaned_data.get('season'),
                                             form.cleaned_data.get('year'))
            new_menu.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('menu:menu_detail', args=[new_menu.pk])
            )
    else:
        form = forms.MenuForm()
    return render(request,
                  'menu/create_menu.html',
                  {'form': form})


@login_required
def edit_menu(request, pk):
    """Edit a menu"""
    menu = models.Menu.objects.get(pk=pk)
    items = models.Item.objects.all()
    if menu.creator != request.user:
        raise Http404
    if request.method == "POST":
        form = forms.MenuForm(
            request.POST,
            instance=menu
        )
        if form.is_valid():
            form.save(commit=False)
            menu.season = '{} {}'.format(form.cleaned_data.get('season'),
                                         form.cleaned_data.get('year'))
            form.save()
            return HttpResponseRedirect(reverse('menu:menu_detail',
                                                args=[menu.pk]))
    else:
        form = forms.MenuForm(
            instance=menu
        )
    return render(request,
                  'menu/edit_menu.html',
                  {'form': form, 'menu': menu, 'items': items,})
