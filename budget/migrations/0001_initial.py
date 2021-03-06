# Generated by Django 3.1.7 on 2021-04-30 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.category')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_id', models.IntegerField()),
                ('date', models.DateField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('product', models.ManyToManyField(to='budget.Product')),
                ('title', models.ManyToManyField(to='budget.Event')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ManyToManyField(to='budget.Group'),
        ),
    ]
