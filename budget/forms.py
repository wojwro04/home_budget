from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='Szukana fraza', max_length=512, required=True)
    exact = forms.BooleanField(label='Dokładne wyszukiwanie', required=False)

class AddEventForm(forms.Form):
    title = forms.CharField(label='Tytuł', max_length=512, required=True)
    expense_date = forms.DateField(label='Data', required=True)
    expense_price = forms.FloatField(label='Cena', required=True)
    expense_amount = forms.FloatField(label='Ilość', required=True)
    expense_product = forms.CharField(label='Nazwa produktu', max_length=512, required=True)
    expense_category = forms.CharField(label='Kategoria', max_length=512, required=True)
    expense_subcategory = forms.CharField(label='Podkategoria', max_length=512, required=True)