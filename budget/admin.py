from django.contrib import admin

from .models import Group, Category, Product, Event, Expense

admin.site.register(Group)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Event)
admin.site.register(Expense)