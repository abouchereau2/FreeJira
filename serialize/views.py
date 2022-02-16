from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
import mimetypes
import os
import ast

from epics.models import *


'''
Parse a dictionary and merge data with database
'''
def import_backlog(dict):
    try:
        for epic_name, data in dict.items():
            cur_epic, created = Epic.objects.get_or_create(title=epic_name)

            for task in data["Tasks"]:
                t, created = Task.objects.update_or_create(title=task, epic=cur_epic)
                t.save()

            for bug in data["Bugs"]:
                b, created = Bug.objects.update_or_create(title=bug, epic=cur_epic)
                b.save()

            for epic in data["Epics"]:
                e, created = Epic.objects.get_or_create(title=epic)
                e.linked_epic = cur_epic
                e.refresh_status()

            cur_epic.refresh_status()
    except:
        return False

    return True


'''
Parse database into a dictionary
'''
def export_backlog():
    dict = {}

    for epic in Epic.objects.all():
        dict[epic.title] = {"Bugs": list(), "Tasks": list(), "Epics": list()}

        for bug in Bug.objects.filter(epic=epic):
            dict[epic.title]["Bugs"].append(bug.title)

        for task in Task.objects.filter(epic=epic):
            dict[epic.title]["Tasks"].append(task.title)

        for linked_epic in Epic.objects.filter(linked_epic=epic):
            dict[epic.title]["Epics"].append(linked_epic.title)

    return dict


'''
Upload a txt file containing a dictionary and import it in database
'''
def simple_upload(request):
    if request.method == 'POST' and 'backlog' in request.FILES:
        try:
            fs = FileSystemStorage()
            file = fs.open(request.FILES['backlog'].name, 'r')
            dictionary = ast.literal_eval(file.read())
            file.close()
        except:
            return render(request, 'index.html', {'import_success': 'Error opening file'})

        if import_backlog(dictionary):
            return render(request, 'index.html', {'import_success': 'Backlog imported'})
        else:
            return render(request, 'index.html', {'import_success': 'Error in backlog import'})

    return render(request, 'index.html')


'''
Export the database in a downloadable text file
'''
def export(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'backlog.txt'
    filepath = BASE_DIR + '/' + filename

    if os.path.exists(filepath):
        with open(filepath, 'w+') as fh:
            fh.write(str(export_backlog()))
            fh.close()

        with open(filepath, 'r') as fh:
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response

    raise Http404


'''
Flush database
'''
def reset(request):
    try:
        Task.objects.all().delete()
        Bug.objects.all().delete()
        Epic.objects.all().delete()
    except:
        return render(request, 'index.html', {'reset_success': 'Error'})

    return render(request, 'index.html', {'reset_success': 'Reset done'})