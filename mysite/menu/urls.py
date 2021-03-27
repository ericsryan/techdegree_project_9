from django.urls import path

from . import views

urlpatterns = [
    path('', views.current_menu_list, name='current_menu_list'),
    path('menu/new/', views.create_menu, name='create_menu'),
    path('menu/<pk>/', views.menu_detail, name='menu_detail'),
    path('menu/item/<pk>/', views.item_detail, name='item_detail'),
    path('menu/edit/<pk>', views.edit_menu, name='menu_edit'),
    path('login', views.sign_in, name='login'),
    path('logout', views.sign_out, name='logout'),
    path('register', views.register, name='register'),
]
