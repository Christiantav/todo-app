from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Category(models.Model): # The Category table name that inherits models.Model
    name = models.CharField(max_length=100) #Like a varchar
    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
    def __str__(self):
        return self.name # name to be shown when called

class Todo(models.Model): # Todolist able name that inherits models.Model
    title = models.CharField(max_length=250) # a varchar
    content = models.TextField(blank=True) # a text field
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # a foreignkey
    completion = models.TextField(blank=True)
    dueness = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ["-created"] # ordering by the created field

    def __str__(self):
        return self.content # name to be shown when called

    def dueness_calculator(self):
        due, now = self.due_date, datetime.date(datetime.now())
        due_days = due - now
        self.dueness = int(due_days.days)
