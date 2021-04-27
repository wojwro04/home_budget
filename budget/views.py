from django.http import HttpResponse
from django.shortcuts import render
import numpy as np

from .models import Categories
from .models import Products
from .models import Expenses

def index(request):
    hello_message = "Witaj!"
    return HttpResponse("%s" % hello_message)

def del_categories(request):
    Categories.objects.all().delete()
    return HttpResponse("Categories - usunięto")

def del_products(request):
    Products.objects.all().delete()
    return HttpResponse("Products - usunięto")
    
def del_expenses(request):
    Expenses.objects.all().delete()
    return HttpResponse("Expenses - usunięto")
    
def categories(request):
    cats = Categories.objects.all()
    lista = ""
    for c in cats:
        lista += f"{c}<br>"
    return HttpResponse("%s" % lista)

def products(request):
    prods = Products.objects.all()
    lista = ""
    for p in prods:
        lista += f"{p}<br>"
    return HttpResponse("%s" % lista)

def expenses(request):
    exps = Expenses.objects.all()
    lista = ""
    for e in exps:
        lista += f"{e}<br>"
    return HttpResponse("%s" % lista)

def add_categories(request):
    categories = np.loadtxt('categories.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for category in categories:
        new_name = category[0]
        new_group = category[1]
        q = Categories.objects.filter(name=new_name)
        if len(q) == 0:
            c = Categories(name=new_name, group=new_group)
            c.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_products(request):
    products = np.loadtxt('products.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for product in products:
        new_name = product[0]
        new_category = product[1]
        q = Products.objects.filter(name=new_name)
        if len(q) == 0:
            c = Categories.objects.get(name=new_category)
            p = Products(name=new_name, category=c)
            p.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_expenses(request):
    expenses = np.loadtxt('expenses.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for expense in expenses:
        new_id = expense[0]
        new_title = expense[1]
        new_date = expense[2]
        new_price = expense[3]
        new_amount = expense[4]
        new_product = expense[5]
        q = Expenses.objects.filter(expense_id=new_id)
        if len(q) == 0:
            p = Products.objects.get(name=new_product)
            e = Expenses(expense_id=new_id, title=new_title, date=new_date, price=new_price, amount=new_amount)
            e.save()
            e.product.add(p)
            e.save()
            log_added += new_title + "<br>"
        else:
            log_excepted = new_title + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))
