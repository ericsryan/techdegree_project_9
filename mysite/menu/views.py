import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from operator import attrgetter

from . import forms
from . import models


def menu_list(request):
    menus = models.Menu.objects.filter(expiration_date__gte=timezone.now()).order_by('-expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = models.Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = models.Item.objects.get_object_or_404(pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = forms.MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    items = models.Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.datetime.strptime(
            request.POST.get('expiration_date', ''),
            '%m/%d/%Y'
            )
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
            'menu': menu,
            'items': items,
        })
