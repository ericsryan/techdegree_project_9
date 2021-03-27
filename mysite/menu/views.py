import datetime

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
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
                    return HttpResponseRedirect(reverse('current_menu_list'))
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
            return HttpResponseRedirect(reverse('current_menu_list'))
    return render(
        request,
        'menu/register.html',
        {'form': form, 'registration_page': 'active'}
    )


def sign_out(request):
    """Log the user out of the site"""
    logout(request)
    messages.success(request, "You've been logged out. Come back soon!")
    return HttpResponseRedirect(reverse('current_menu_list'))


def current_menu_list(request):
    """Display a list of current menus."""
    menus = models.Menu.objects.filter(
        expiration_date__gte=timezone.now()
    ).order_by('-expiration_date')
    return render(request,
                  'menu/current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    """Display the detailes of a menu"""
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request,
                  'menu/menu_detail.html',
                  {'menu': menu})


def item_detail(request, pk):
    """Display the details of an item"""
    item = get_object_or_404(models.Item, pk=pk)
    return render(request,
                  'menu/item_detail.html',
                  {'item': item})


def create_menu(request):
    """Create a new menu"""
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(data=request.POST)
        if form.is_valid():
            new_menu = form.save()
            return HttpResponseRedirect(
                reverse('menu_detail', args=[new_menu.pk])
            )
    else:
        form = forms.MenuForm()
    return render(request,
                  'menu/create_menu.html',
                  {'form': form})


def edit_menu(request, pk):
    """Edit a menu"""
    menu = models.Menu.objects.get(pk=pk)
    items = models.Item.objects.all()
    if request.method == "POST":
        form = forms.MenuForm(
            request.POST,
            instance=menu
        )
        form.save()
        return HttpResponseRedirect(reverse('menu_detail', args=[menu.pk]))
    else:
        form = forms.MenuForm(
            instance=menu
        )
    return render(request,
                  'menu/edit_menu.html',
                  {'form': form, 'menu': menu, 'items': items,})
