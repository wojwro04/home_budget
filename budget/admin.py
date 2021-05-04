from django.contrib import admin

from .models import Category, Subcategory, Product, Event, Expense

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Event)
admin.site.register(Expense)