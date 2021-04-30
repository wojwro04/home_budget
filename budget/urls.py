from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups, name='groups'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('events/', views.events, name='events'),
    path('expenses/', views.expenses, name='expenses'),
    path('del_groups/', views.del_groups, name='del_groups'),
    path('del_categories/', views.del_categories, name='del_categories'),
    path('del_products/', views.del_products, name='del_products'),
    path('del_events/', views.del_events, name='del_events'),
    path('del_expenses/', views.del_expenses, name='del_expenses'),
    path('add_groups/', views.add_groups, name='add_groups'),
    path('add_categories/', views.add_categories, name='add_categories'),
    path('add_products/', views.add_products, name='add_products'),
    path('add_events/', views.add_events, name='add_events'),
    path('add_expenses/', views.add_expenses, name='add_expenses'),
    
]