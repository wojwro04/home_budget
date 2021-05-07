from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=512)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=512)
    product = models.ManyToManyField(Product, null=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=512)
    subcategory = models.ManyToManyField(Subcategory, null=True)
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    expense_id = models.IntegerField()
    date = models.DateField()
    price = models.FloatField()
    amount = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.expense_id)

class Event(models.Model):
    title = models.CharField(max_length=512)
    expense = models.ManyToManyField(Expense, null=True)
    
    def __str__(self):
        return self.title

