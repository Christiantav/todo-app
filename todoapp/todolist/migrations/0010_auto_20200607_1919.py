# Generated by Django 3.0.6 on 2020-06-07 19:19

from django.db import migrations, models
import todolist.models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0009_auto_20200607_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='dueness',
            field=models.IntegerField(blank=True, default=todolist.models.Todo.dueness_calculator),
        ),
    ]