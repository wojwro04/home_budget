# Generated by Django 3.1.7 on 2021-05-04 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20210504_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='expense',
            field=models.ManyToManyField(null=True, to='budget.Expense'),
        ),
    ]
