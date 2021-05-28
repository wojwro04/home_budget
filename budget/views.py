from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
import io, base64
from django.db.models import Q


from .models import Category
from .models import Subcategory
from .models import Product
from .models import Event
from .models import Expense
from .forms import SearchForm
from .forms import AddEventForm
from .forms import AddExpenseForm
from .forms import PlotProductForm
from .forms import PlotExpensesForm
from .forms import PlotProductBarForm

def plots(request):
    template = loader.get_template('budget/plots.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def plot_product(request):
    if request.method == 'POST':
        form = PlotProductForm(request.POST)
        if form.is_valid():
            p = request.POST['product']
            expenses = Expense.objects.filter(product=Product.objects.get(name=p))
            return plot(request, expenses)
    else:
        form = PlotProductForm()
    template = loader.get_template('budget/plot_product.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def plot(request, expenses): #jak zmieniała się cena produktu
    d = {}
    for exp in expenses:
        #print(f"--{exp} | {exp.date} | {exp.price}")
        if exp.date in d.keys():
            d[exp.date].append(exp.price)
        else:
            d[exp.date] = []
            d[exp.date].append(exp.price)
    labels = sorted(list(d.keys()))
    x = np.arange(len(labels))
    sizes = []
    for lab in labels:
        sizes.append(np.mean(d[lab]))
    fig1, ax1 = pl.subplots()
    rects1 = ax1.plot(x, sizes)
    rects2 = ax1.plot(x, sizes, 'bo')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    context = {
        'chart': b64,
    }
    
    template = loader.get_template('budget/plot.html')
    return HttpResponse(template.render(context, request))
    
def plot_product_bar(request):
    if request.method == 'POST':
        form = PlotProductBarForm(request.POST)
        if form.is_valid():
            if request.POST['choice_field'] == 'full':
                if request.POST['title']:
                    r = request.POST['title']
                    expenses = Expense.objects.filter(product=Product.objects.get(name=r))
                    return plot2(request, expenses, r)
            if request.POST['choice_field'] == 'detail':
                if request.POST['title']:
                    r = request.POST['title']
                    expenses = Expense.objects.filter(product=Product.objects.get(name=r))
                    return plot3(request, expenses, r)
    else:
        form = PlotProductBarForm()
    template = loader.get_template('budget/plot_product_bar.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def plot2(request, expenses, headline): #kiedy była naprawa samochodu, koszt naprawy
    d = {}
    for exp in expenses:
        #print(f"--{exp} | {exp.date} | {exp.price}")
        if exp.date in d.keys():
            d[exp.date].append(exp.price)
        else:
            d[exp.date] = []
            d[exp.date].append(exp.price)
    labels = sorted(list(d.keys()))
    x = np.arange(len(labels))
    sizes = []
    for lab in labels:
        sizes.append(np.mean(d[lab]))

    fig1, ax1 = pl.subplots()
    width = 0.5
    rects = ax1.bar(x, sizes, width)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    template = loader.get_template('budget/plot.html')
    context = {
        'chart': b64,
        'headline': headline,
    }
    return HttpResponse(template.render(context, request))

def plot3(request, expenses, headline): # ile razy w roku była naprawa samochodu, suma kosztów napraw
    d = {}
    for exp in expenses:
        #print(f"--{exp} | {exp.date.year} | {exp.price}")
        if exp.date.year in d.keys():
            d[exp.date.year].append(exp.price)
        else:
            d[exp.date.year] = []
            d[exp.date.year].append(exp.price)
    labels = sorted(list(d.keys()))
    x = np.arange(len(labels))
    sizes = []
    h_labels = []
    for lab in labels:
        sizes.append(np.sum(d[lab]))
        h_labels.append(len(d[lab]))
    
    fig1, ax1 = pl.subplots()
    width = 0.5
    rects = ax1.bar(x, sizes, width)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    i = 0
    for value in rects:
        height = value.get_height()
        ax1.text(value.get_x() + value.get_width()/2.,1.002*height,'%d' % int(h_labels[i]), ha='center', va='bottom')
        i += 1
    
    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    template = loader.get_template('budget/plot.html')
    context = {
        'chart': b64,
        'headline': headline,
    }
    return HttpResponse(template.render(context, request))

def plot_expenses(request):
    if request.method == 'POST':
        form = PlotExpensesForm(request.POST)
        if form.is_valid():
            if request.POST['choice_field'] == 'category':
                expenses = Expense.objects.all()
                return plot4(request, expenses)
            if request.POST['choice_field'] == 'subcategory':
                if request.POST['category_title']:
                    r = request.POST['category_title']
                    wanted_category = r
                    expenses = Expense.objects.filter(category=Category.objects.get(name=wanted_category))
                    return plot5(request, expenses)
            if request.POST['choice_field'] == 'product':
                if request.POST['subcategory_title']:
                    r = request.POST['subcategory_title']
                    expenses = Expense.objects.filter(subcategory=Subcategory.objects.get(name=r))
                    return plot6(request, expenses)
    else:
        form = PlotExpensesForm()
    template = loader.get_template('budget/plot_expenses.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def plot4(request, expenses): #wykres kołowy - wydatki na kategorie
    d = {}
    for exp in expenses:
        cat = Category.objects.get(expense=exp)
        if cat.name in d.keys():
            d[cat.name].append(exp.price * exp.amount)
        else:
            d[cat.name] = []
            d[cat.name].append(exp.price * exp.amount)
    
    labels = list(d.keys())
    sizes = []
    for lab in labels:
        sizes.append(np.sum(d[lab]))

    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = pl.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)#, explode=explode)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    context = {
        'chart': b64,
    }
    
    template = loader.get_template('budget/plot.html')
    return HttpResponse(template.render(context, request))
    
def plot5(request, expenses): #wykres kołowy - wydatki w kategorii jedzenie
    d = {}
    for exp in expenses:
        prod = Product.objects.get(expense=exp)
        subcat = Subcategory.objects.get(expense=exp)
        if subcat.name in d.keys():
            d[subcat.name].append(exp.price * exp.amount)
        else:
            d[subcat.name] = []
            d[subcat.name].append(exp.price * exp.amount)
    
    labels = list(d.keys())
    sizes = []
    for lab in labels:
        sizes.append(np.sum(d[lab]))

    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = pl.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)#, explode=explode)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    context = {
        'chart': b64,
    }
    template = loader.get_template('budget/plot.html')
    return HttpResponse(template.render(context, request))

def plot6(request, expenses): #wykres kołowy - wydatki w podkategorii nabiał
    d = {}
    for exp in expenses:
        prod = Product.objects.get(expense=exp)
        if prod.name in d.keys():
            d[prod.name].append(exp.price * exp.amount)
        else:
            d[prod.name] = []
            d[prod.name].append(exp.price * exp.amount)
    
    labels = list(d.keys())
    sizes = []
    for lab in labels:
        sizes.append(np.sum(d[lab]))

    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = pl.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)#, explode=explode)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    flike = io.BytesIO()
    fig1.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()

    context = {
        'chart': b64,
    }
    template = loader.get_template('budget/plot.html')
    return HttpResponse(template.render(context, request))
    
#######################################################

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
            if request.POST['choice_field'] == 'all':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return product(request, request.POST['title'])
                        except Product.DoesNotExist:
                            try:
                                return expense(request, request.POST['title'])
                            except Expense.DoesNotExist:
                                try:
                                    return event(request, request.POST['title'])
                                except Event.DoesNotExist:
                                    products = []
                                    return search_results_products(request, products)
                    else:
                        products = Product.objects.filter(name__contains=request.POST['title'])
                        expenses = Expense.objects.filter(Q(expense_id__contains=request.POST['title']) | Q(product__in=products))
                        events = Event.objects.filter(Q(title__contains=request.POST['title']) | Q(expense__in=expenses))
                        return search_results(request, products, expenses, events)
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
                        products = Product.objects.filter(name__contains=request.POST['title'])
                        expenses = Expense.objects.filter(Q(expense_id__contains=request.POST['title']) | Q(product__in=products))
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
                        products = Product.objects.filter(name__contains=request.POST['title'])
                        expenses = Expense.objects.filter(product__in=products)
                        events = Event.objects.filter(Q(title__contains=request.POST['title']) | Q(expense__in=expenses))
                        return search_results_events(request, events)
    else:
        form = SearchForm()
    template = loader.get_template('budget/search.html')
    return HttpResponse(template.render({'form': form}, request))

def search_results(request, products, expenses, events):
    template = loader.get_template('budget/search_results.html')
    context = {
        'products': products,
        'expenses': expenses,
        'events': events,
    }
    return HttpResponse(template.render(context, request))

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

def delete(request):
    Product.objects.all().delete()
    Subcategory.objects.all().delete()
    Category.objects.all().delete()
    Expense.objects.all().delete()
    Event.objects.all().delete()
    return HttpResponse("Budget - usunięto")
    
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

def add_event(request):
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            e = Event(title=request.POST['title'])
            e.save()
            # expenses = list(Expense.objects.all())
            # p =Product.objects.get(name=request.POST['expense_product'])
            # ex_id = int(expenses[-1].expense_id) + 1
            # ex = Expense(expense_id=ex_id, date=request.POST['expense_date'], price=request.POST['expense_price'], amount=request.POST['expense_amount'], product=p, subcategory=request.POST['expense_subcategory'], category=request.POST['expense_category'])
            # ex.save()
            return add_expense(request, request.POST['title'])
    else:
        form = AddEventForm()
    template = loader.get_template('budget/add_event.html')
    return HttpResponse(template.render({'form': form}, request))

def add_expense(request, event_title):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        #if form.is_valid():
        e = Event.objects.get(title=event_title)
        p = Product.objects.get(name=request.POST['expense_product'])
        ex_id = int(expenses[-1].expense_id) + 1
        ex = Expense(expense_id=ex_id, date=request.POST['expense_date'], price=request.POST['expense_price'], amount=request.POST['expense_amount'], product=p, subcategory=request.POST['expense_subcategory'], category=request.POST['expense_category'])
        ex.save()
        return add_result(request, request.POST['title'])
    else:
        form = AddExpenseForm()
    template = loader.get_template('budget/add_event.html')
    return HttpResponse(template.render({'form': form}, request))

def add_result(request, title):
    template = loader.get_template('budget/add_result.html')
    context = {
        'title': title,
    }
    return HttpResponse(template.render(context, request))

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
            sc = Subcategory.objects.get(product=p)
            c = Category.objects.get(subcategory=sc)
            e = Expense(expense_id=new_id, date=new_date, price=new_price, amount=new_amount, product=p, subcategory=sc, category=c)
            e.save()
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

def add_all(request):
    products = add_products(request)
    subcategories = add_subcategories(request)
    categories = add_categories(request)
    expenses = add_expenses(request)
    events = add_events(request)
    return HttpResponse("Budget - dodano")