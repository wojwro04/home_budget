from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=512)
    
    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=512)
    category = models.ManyToManyField(Category, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=512)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=512)
    
    def __str__(self):
        return self.title

class Expense(models.Model):
    expense_id = models.IntegerField()
    date = models.DateField()
    price = models.FloatField()
    amount = models.FloatField()
    product = models.ManyToManyField(Product, null=True)
    title = models.ManyToManyField(Event, null=True)
    
    def __str__(self):
        return str(self.expense_id)

