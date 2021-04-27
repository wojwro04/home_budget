from django.contrib import admin

from .models import Categories, Products, Expenses

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Expenses)