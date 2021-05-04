from django.http import HttpResponse
from django.shortcuts import render
import numpy as np

from .models import Category
from .models import Subcategory
from .models import Product
from .models import Event
from .models import Expense

def index(request):
    hello_message = "Witaj!"
    return HttpResponse("%s" % hello_message)

def del_categories(request):
    Category.objects.all().delete()
    return HttpResponse("Category - usunięto")

def del_subcategories(request):
    Subcategory.objects.all().delete()
    return HttpResponse("Subcategory - usunięto")

def del_products(request):
    Product.objects.all().delete()
    return HttpResponse("Product - usunięto")
    
def del_events(request):
    Event.objects.all().delete()
    return HttpResponse("Event - usunięto")
    
def del_expenses(request):
    Expense.objects.all().delete()
    return HttpResponse("Expense - usunięto")
    
def categories(request):
    cats = Categories.objects.all()
    lista = ""
    for c in cats:
        lista += f"{c}<br>"
    return HttpResponse("%s" % lista)

def subcategories(request):
    scats = Subcategories.objects.all()
    lista = ""
    for s in scats:
        lista += f"{s}<br>"
    return HttpResponse("%s" % lista)

def products(request):
    prods = Products.objects.all()
    lista = ""
    for p in prods:
        lista += f"{p}<br>"
    return HttpResponse("%s" % lista)

def events(request):
    evs = Event.objects.all()
    lista = ""
    for e in evs:
        lista += f"{e}<br>"
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
        new_name = category
        q = Category.objects.filter(name=new_name)
        if len(q) == 0:
            c = Category(name=new_name)
            c.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))
    
def add_subcategories(request):
    subcategories = np.loadtxt('subcategories.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for subcategory in subcategories:
        new_name = subcategory[0]
        new_group = subcategory[1]
        q = Subcategory.objects.filter(name=new_name)
        if len(q) == 0:
            c = Category.objects.get(name=new_group)
            s = Subcategory(name=new_name)
            s.save()
            s.category.add(c)
            s.save()
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
        q = Product.objects.filter(name=new_name)
        if len(q) == 0:
            c = Subcategory.objects.get(name=new_category)
            p = Product(name=new_name, subcategory=c)
            p.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_events(request):
    events = np.loadtxt('events.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for event in events:
        new_title = event
        q = Event.objects.filter(title=new_title)
        if len(q) == 0:
            e = Event(title=new_title)
            e.save()
            log_added += new_title + "<br>"
        else:
            log_excepted = new_title + "<br>"
        
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
        q = Expense.objects.filter(expense_id=new_id)
        if len(q) == 0:
            p = Product.objects.get(name=new_product)
            ev = Event.objects.get(title=new_title)
            e = Expense(expense_id=new_id, date=new_date, price=new_price, amount=new_amount)
            e.save()
            e.product.add(p)
            e.save()
            e.title.add(ev)
            e.save()
            log_added += new_title + "<br>"
        else:
            log_excepted = new_title + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))
