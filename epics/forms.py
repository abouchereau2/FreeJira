from django import forms
from django.forms import ModelForm

from .models import Epic, Bug, Task

'''
Create a ModelForm for bug
'''
class BugForm(ModelForm):
    class Meta:
        model = Bug
        fields = ['title']

'''
Create a ModelForm for task
'''
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title']