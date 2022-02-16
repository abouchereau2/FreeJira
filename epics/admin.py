from django.contrib import admin

from .models import Epic, Task, Bug

admin.site.register(Epic)
admin.site.register(Task)
admin.site.register(Bug)