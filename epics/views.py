from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from .models import Epic, Bug, Task
from .forms import BugForm, TaskForm


'''
List of all epics
'''
def all_epics(request):
    epics = Epic.objects.all()

    return render(request, "epics.html", {"epics": epics})


'''
Detail view of one epic
'''
def one_epic(request, epic_id):
    epic = get_object_or_404(Epic, id=epic_id)

    bugs = epic.get_bugs()
    tasks = epic.get_tasks()
    linked_epics = epic.get_children_epics()
    linked_bugs = epic.get_linked_bugs()

    return render(request, "epic.html", {"epic": epic, "bugs": bugs, "tasks": tasks, "linked_epics": linked_epics, "linked_bugs": linked_bugs})


'''
Form to add a bug to an epic
'''
def add_bug(request, epic_id):
    epic = get_object_or_404(Epic, id=epic_id)

    if request.method == "POST":
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.epic = epic
            bug.save()
            epic.refresh_status()
            return redirect('epics:epic', epic_id=epic.id)
    else:
        form = BugForm()

    return render(request, 'add_bug.html', {'form': form})


'''
Form to add a task to an epic
'''
def add_task(request, epic_id):
    epic = get_object_or_404(Epic, id=epic_id)

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.epic = epic
            task.save()
            epic.refresh_status()
            return redirect('epics:epic', epic_id=epic.id)
    else:
        form = BugForm()

    return render(request, 'add_task.html', {'form': form})


'''
Delete a bug of an epic and refresh its status
'''
def delete_bug(request, epic_id, bug_id):
    bug = get_object_or_404(Bug, pk=bug_id)
    epic = Epic.objects.get(pk=epic_id)

    #Redirect to the current epic url
    redir_url = reverse(
        'epics:epic', 
        kwargs={'epic_id': epic.pk}
    )

    bug.delete()
    epic.refresh_status()

    return redirect(redir_url)


'''
Delete a task of an epic and refresh its status
'''
def delete_task(request, epic_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    epic = Epic.objects.get(pk=epic_id)

    #Redirect to the current epic url
    redir_url = reverse(
        'epics:epic', 
        kwargs={'epic_id': epic.pk}
    )

    task.delete()
    epic.refresh_status()

    return redirect(redir_url)