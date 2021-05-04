from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('products/', views.products, name='products'),
    path('product/<str:product>/', views.product, name='product'),
    path('subcategories/', views.subcategories, name='subcategories'),
    path('subcategory/<str:subcategory>/', views.subcategory, name='subcategory'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:category>/', views.category, name='category'),
    path('expenses/', views.expenses, name='expenses'),
    path('expense/<str:expense>/', views.expense, name='expense'),
    path('events/', views.events, name='events'),
    path('event/<str:event>/', views.event, name='event'),
    path('del_products/', views.del_products, name='del_products'),
    path('del_subcategories/', views.del_subcategories, name='del_subcategories'),
    path('del_categories/', views.del_categories, name='del_categories'),
    path('del_expenses/', views.del_expenses, name='del_expenses'),
    path('del_events/', views.del_events, name='del_events'),
    path('add_categories/', views.add_categories, name='add_categories'),
    path('add_subcategories/', views.add_subcategories, name='add_subcategories'),
    path('add_products/', views.add_products, name='add_products'),
    path('add_events/', views.add_events, name='add_events'),
    path('add_expenses/', views.add_expenses, name='add_expenses'),
    
]