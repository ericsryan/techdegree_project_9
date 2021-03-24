import datetime


from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from . import forms
from . import models


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
