from django import forms
from .models import Category
from .models import Subcategory

class SearchForm(forms.Form):
    choices = (
        ('all', 'Wszystko'),
        ('product', 'Produkty'),
        ('expense', 'Wydatki'),
        ('event', 'Wydarzenia'),
    )
    choice_field = forms.ChoiceField(label='Zakres wyszukiwania', choices=choices, widget=forms.RadioSelect(), initial='all')
    title = forms.CharField(label='Szukana fraza', max_length=512, required=True)
    exact = forms.BooleanField(label='Dokładne wyszukiwanie', required=False)

class AddEventForm(forms.Form):
    title = forms.CharField(label='Tytuł', max_length=512, required=True)
    
class AddExpenseForm(forms.Form):
    date = forms.DateField(label='Data', required=True)
    price = forms.FloatField(label='Cena', required=True)
    amount = forms.FloatField(label='Ilość', required=True)
    product = forms.CharField(label='Nazwa produktu', max_length=512, required=True)
    category = forms.CharField(label='Kategoria', max_length=512, required=True)
    subcategory = forms.CharField(label='Podkategoria', max_length=512, required=True)

class PlotProductForm(forms.Form):
    product = forms.CharField(label='Nazwa produktu', max_length=512, required=True)
    
class PlotExpensesForm(forms.Form):
    choices = (
        ('category', 'Kategorie'),
        ('subcategory', 'Podkategorie (wybierz kategorię)'),
        ('product', 'Produkt (wybierz podkategorię)'),
    )
    choice_field = forms.ChoiceField(label='Zakres', choices=choices, widget=forms.RadioSelect(), initial='category')
    
    categories = Category.objects.all()
    category_choices = []
    for c in categories:
        category_choices.append((str(c),str(c)))
    category_title = forms.CharField(label='Wybór kategorii', widget = forms.Select(choices=category_choices))
    
    subcategory_choices = []
    for c in categories:
        subcategories = Subcategory.objects.filter(category=c)
        cat = [str(c),[]]
        for s in subcategories:
            cat[1].append( (str(s), str(s)) )
        subcategory_choices.append(cat)
    subcategory_title = forms.CharField(label='Wybór podkategorii', widget = forms.Select(choices=subcategory_choices))
    #title = forms.CharField(label='Tytuł', max_length=512)

class PlotProductBarForm(forms.Form):
    choices = (
        ('full', 'Ogólny'),
        ('detail', 'Szczegółowy'),
    )
    choice_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(), initial='full')
    title = forms.CharField(label='Tytuł', max_length=512)