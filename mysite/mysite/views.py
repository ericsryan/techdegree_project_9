from django.shortcuts import render
from django.utils import timezone

from menu import models

def index(request):
    """Display a list of current menus."""
    menus = models.Menu.objects.filter(
        expiration_date__gte=timezone.now()
    ).prefetch_related(
        'items'
    ).order_by('-expiration_date')
    return render(request,
                  'index.html',
                  {'menus': menus})
