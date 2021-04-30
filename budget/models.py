from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    group = models.ManyToManyField(Group)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

class Expense(models.Model):
    expense_id = models.IntegerField()
    date = models.DateField()
    price = models.FloatField()
    amount = models.FloatField()
    product = models.ManyToManyField(Product)
    title = models.ManyToManyField(Event)
    
    def __str__(self):
        return self.expense_id

