from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import numpy as np

from .models import Category
from .models import Subcategory
from .models import Product
from .models import Event
from .models import Expense
from .forms import SearchForm


def index(request):
    template = loader.get_template('budget/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

#######################################################

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if request.POST['choice_field'] == 'product':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return product(request, request.POST['title'])
                        except Product.DoesNotExist:
                            products = []
                            return search_results_products(request, products)
                    else:                
                        products = Product.objects.filter(name__contains=request.POST['title'])
                        return search_results_products(request, products)
            if request.POST['choice_field'] == 'expense':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return expense(request, request.POST['title'])
                        except Expense.DoesNotExist:
                            expenses = []
                            return search_results_expenses(request, expenses)
                    else:                
                        expenses = Expense.objects.filter(expense_id__contains=request.POST['title'])
                        return search_results_expenses(request, expenses)
            if request.POST['choice_field'] == 'event':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return event(request, request.POST['title'])
                        except Event.DoesNotExist:
                            events = []
                            return search_results_events(request, events)
                    else:                
                        events = Event.objects.filter(title__contains=request.POST['title'])
                        return search_results_events(request, events)
    else:
        form = SearchForm()
    template = loader.get_template('budget/search.html')
    return HttpResponse(template.render({'form': form}, request))

def search_results_products(request, products):
    template = loader.get_template('budget/search_results_products.html')
    context = {
        'products': products,
    }
    return HttpResponse(template.render(context, request))

def search_results_expenses(request, expenses):
    template = loader.get_template('budget/search_results_expenses.html')
    context = {
        'expenses': expenses,
    }
    return HttpResponse(template.render(context, request))

def search_results_events(request, events):
    template = loader.get_template('budget/search_results_events.html')
    context = {
        'events': events,
    }
    return HttpResponse(template.render(context, request))

#######################################################

def del_products(request):
    Product.objects.all().delete()
    return HttpResponse("Product - usunięto")
    
def del_subcategories(request):
    Subcategory.objects.all().delete()
    return HttpResponse("Subcategory - usunięto")

def del_categories(request):
    Category.objects.all().delete()
    return HttpResponse("Category - usunięto")

def del_expenses(request):
    Expense.objects.all().delete()
    return HttpResponse("Expense - usunięto")
    
def del_events(request):
    Event.objects.all().delete()
    return HttpResponse("Event - usunięto")

#######################################################

def products(request):
    products = Product.objects.all()
    template = loader.get_template('budget/products.html')
    context = {
        'products': products,
    }
    return HttpResponse(template.render(context, request))

def product(request, product):
    product = Product.objects.get(name=product)
    subcategory = Subcategory.objects.get(product=product)
    category = Category.objects.get(subcategory=subcategory)
    template = loader.get_template('budget/product.html')
    context = {
        'product': product,
        'subcategory': subcategory,
        'category': category,
    }
    return HttpResponse(template.render(context, request))
    
def subcategories(request):
    subcategories = Subcategory.objects.all()
    template = loader.get_template('budget/subcategories.html')
    context = {
        'subcategories': subcategories,
    }
    return HttpResponse(template.render(context, request))

def subcategory(request, subcategory):
    subcategory = Subcategory.objects.get(name=subcategory)
    category = Category.objects.get(subcategory=subcategory)
    product_list = Product.objects.filter(subcategory=subcategory)
    template = loader.get_template('budget/subcategory.html')
    context = {
        'subcategory': subcategory,
        'category': category,
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def categories(request):
    categories = Category.objects.all()
    template = loader.get_template('budget/categories.html')
    context = {
        'categories': categories,
    }
    return HttpResponse(template.render(context, request))

def category(request, category):
    category = Category.objects.get(name=category)
    subcategory_list = Subcategory.objects.filter(category=category)
    template = loader.get_template('budget/category.html')
    context = {
        'subcategory_list': subcategory_list,
        'category': category,
    }
    return HttpResponse(template.render(context, request))

def expenses(request):
    expenses = Expense.objects.all()
    template = loader.get_template('budget/expenses.html')
    context = {
        'expenses': expenses,
    }
    return HttpResponse(template.render(context, request))

def expense(request, expense):
    expense = Expense.objects.get(expense_id=expense)
    product = Product.objects.get(expense=expense)
    template = loader.get_template('budget/expense.html')
    context = {
        'expense': expense,
        'product': product,
    }
    return HttpResponse(template.render(context, request))

def events(request):
    events = Event.objects.all()
    template = loader.get_template('budget/events.html')
    context = {
        'events': events,
    }
    return HttpResponse(template.render(context, request))

def event(request, event):
    event = Event.objects.get(title=event)
    expense_list = Expense.objects.filter(event=event)
    template = loader.get_template('budget/event.html')
    context = {
        'event': event,
        'expense_list': expense_list,
    }
    return HttpResponse(template.render(context, request))
    
#######################################################

def add_products(request):
    products = np.loadtxt('products.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for product in products:
        new_name = product[0]
        q = Product.objects.filter(name=new_name)
        if len(q) == 0:
            p = Product(name=new_name)
            p.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_subcategories(request):
    subcategories = np.loadtxt('subcategories.txt', delimiter=',', dtype='str')
    products = np.loadtxt('products.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for subcategory in subcategories:
        new_name = subcategory[0]
        q = Subcategory.objects.filter(name=new_name)
        if len(q) == 0:
            s = Subcategory(name=new_name)
            s.save()
            for product in products:
                pr_name = product[0]
                pr_subcategory = product[1]
                if pr_subcategory == new_name:
                    p = Product.objects.get(name=pr_name)
                    s.product.add(p)
                    s.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_categories(request):
    categories = np.loadtxt('categories.txt', delimiter=',', dtype='str')
    subcategories = np.loadtxt('subcategories.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for category in categories:
        new_name = category
        q = Category.objects.filter(name=new_name)
        if len(q) == 0:
            c = Category(name=new_name)
            c.save()
            for subcategory in subcategories:
                s_name = subcategory[0]
                s_category = subcategory[1]
                if s_category == new_name:
                    s = Subcategory.objects.get(name=s_name)
                    c.subcategory.add(s)
                    c.save()
            log_added += new_name + "<br>"
        else:
            log_excepted = new_name + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))
    
def add_expenses(request):
    expenses = np.loadtxt('expenses.txt', delimiter=',', dtype='str')
    products = np.loadtxt('products.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for expense in expenses:
        new_id = expense[0]
        new_date = expense[2]
        new_price = expense[3]
        new_amount = expense[4]
        new_product = expense[5]
        q = Expense.objects.filter(expense_id=new_id)
        if len(q) == 0:
            p = Product.objects.get(name=new_product)
            e = Expense(expense_id=new_id, date=new_date, price=new_price, amount=new_amount, product=p)
            e.save()
            # for product in products:
                # pr_name = product[0]
                # if pr_name == new_product:
                    
                    # e.product.add(p)
                    # e.save()
            log_added += new_id + "<br>"
        else:
            log_excepted = new_id + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

def add_events(request):
    events = np.loadtxt('events.txt', delimiter=',', dtype='str')
    expenses = np.loadtxt('expenses.txt', delimiter=',', dtype='str')
    log_added = ""
    log_excepted = ""
    for event in events:
        new_title = event
        q = Event.objects.filter(title=new_title)
        if len(q) == 0:
            e = Event(title=new_title)
            e.save()
            for expense in expenses:
                ex_id = expense[0]
                ex_title = expense[1]
                if ex_title == new_title:
                    ex = Expense.objects.get(expense_id=ex_id)
                    e.expense.add(ex)
                    e.save()
            log_added += new_title + "<br>"
        else:
            log_excepted = new_title + "<br>"
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (log_excepted,log_added))

