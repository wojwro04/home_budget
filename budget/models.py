from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Expenses(models.Model):
    expense_id = models.IntegerField()
    title = models.CharField(max_length=512)
    date = models.DateField()
    price = models.FloatField()
    amount = models.FloatField()
    product = models.ManyToManyField(Products)

    def __str__(self):
        return self.title