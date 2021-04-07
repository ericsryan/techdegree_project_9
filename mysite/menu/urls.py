from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('new/', views.create_menu, name='create_menu'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.register, name='register'),
    path('<pk>/', views.menu_detail, name='menu_detail'),
    path('item/<pk>/', views.item_detail, name='item_detail'),
    path('edit/<pk>/', views.edit_menu, name='edit_menu'),
]
