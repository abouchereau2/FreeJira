from django.shortcuts import render
from epics.models import *


'''
Perform search on bug title and return all parent epics
'''
def do_search(request):
    r = {}
    bugs = Bug.objects.filter(title__icontains=request.GET['q'])

    #For each bug containing the search word
    for bug in bugs:
        epics = []

        #Retrieve all parent epics
        parent_epics = bug.epic.get_parent_epics_recursive(include_self=True)

        #And add them to a list
        for epic in parent_epics:
            epics.append(epic)

        #Reverse the epics list because we want the highest epic in the tree in first position
        #Then add list to dictionnary
        epics.reverse()
        r[bug.title] = list()
        r[bug.title].extend(epics)

    return render(request, 'results.html', {'bugs': r})