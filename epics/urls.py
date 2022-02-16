from django.urls import path
from .views import *


app_name = 'epics'
urlpatterns = [
    #List of epics
    path('', all_epics, name='epics'),
    #Detail view of one epic
    path('<int:epic_id>/', one_epic, name='epic'),
    #Add a bug to an epic
    path('<int:epic_id>/bug/', add_bug, name='add_bug'),
    #Add a task to an epic
    path('<int:epic_id>/task/', add_task, name='add_task'),
    #Delete a bug of an epic
    path('<int:epic_id>/delete_bug/<int:bug_id>/', delete_bug, name='delete_bug'),
    #Delete a task of an epic
    path('<int:epic_id>/delete_task/<int:task_id>/', delete_task, name='delete_task')
]
