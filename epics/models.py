from django.db import models


STATES = (('completed', 'Completed'),
         ('in_progress', 'Work in progress'),
         ('pending', 'Pending validation'))


class Epic(models.Model):

    title = models.CharField(max_length=64, default=' ', blank=False, unique=True)
    state = models.CharField(max_length=64, choices=STATES, default='completed')
    linked_epic = models.ForeignKey('epics.Epic', on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='epic')


    def __str__(self):
        return self.title

    '''
    Get list of children bugs
    '''
    def get_bugs(self):
        return Bug.objects.filter(epic=self.pk)

    '''
    Get list of children tasks
    '''
    def get_tasks(self):
        return Task.objects.filter(epic=self.pk)
    
    '''
    Get list of children epics
    '''
    def get_children_epics(self):
        return Epic.objects.filter(linked_epic=self.pk)

    '''
    Get list of children epics through all tree
    '''
    def get_children_epics_recursive(self, include_self=True):
        r = []

        if include_self:
            r.append(self)
        for epic in self.get_children_epics():
            _r = epic.get_children_epics_recursive(include_self=True)
            if 0 < len(_r):
                r.extend(_r)

        return r

    '''
    Get list of parent epics through all tree
    '''
    def get_parent_epics_recursive(self, include_self=True):
        r = []

        if include_self:
            r.append(self)
        if self.linked_epic:
            _r = self.linked_epic.get_parent_epics_recursive(include_self=True)
            if 0 < len(_r):
                r.extend(_r)

        return r

    '''
    Get list of bugs owned by all children epics
    '''
    def get_linked_bugs(self):
        r = []

        for epic in self.get_children_epics_recursive(False):
            bugs = Bug.objects.filter(epic=epic.pk)
            for bug in bugs:
                r.append(bug.title)

        return r


    '''
    An epic is 'completed' if it has no pending tasks and bugs and it depends on no other epic
    '''
    def is_completed(self) -> bool:
        #Epic has no Tasks*
        if Task.objects.filter(epic=self).count() != 0: 
            return False
        #No Bugs
        if Bug.objects.filter(epic=self).count() != 0: 
            return False
        #All linked Epics are "completed"
        for epic in Epic.objects.filter(linked_epic=self):
            if 'completed' not in epic.state:
                return False
        return True

    '''
    An epic is 'work in progress' if it contains any tasks or if any of its linked epics is 'work in progress'
    '''
    def is_work_in_progress(self) -> bool:
        #Epic has at least one Task or one linked Epic at "work in progress"
        return Task.objects.filter(epic=self).count() > 0 or Epic.objects.filter(linked_epic=self, state='in_progress').count() > 0

    '''
    An epic is 'pending' if it has no tasks but still bugs, or if any of its linked epics is 'pending'
    '''
    def is_pending(self):
        #Epic has no Tasks
        if Task.objects.filter(epic=self).count() != 0: 
            return False

        for epic in Epic.objects.filter(linked_epic=self):
            #If one linked epic is 'pending', current epic is 'pending'
            if 'pending' in epic.state:
                return True
            #If one linked epic is 'in progress', current epic is 'in progress'
            if 'in_progress' in epic.state:
                return False

        #Has at least one bug pending
        if Bug.objects.filter(epic=self).count() == 0: 
            return False

        return True

    '''
    Refresh the current status of an epic
    Refresh also its parent linked epic
    '''
    def refresh_status(self):
        if self.is_completed():
            self.state = 'completed'
        elif self.is_pending(): 
            self.state = 'pending'
        elif self.is_work_in_progress(): 
            self.state = 'in_progress'
        else: 
            self.state = None

        self.save()

        for epic in self.get_parent_epics_recursive(include_self=False):
            epic.refresh_status()
            #epic.save()


class Task(models.Model):

    title = models.CharField(max_length=64, default=' ', blank=False, unique=True)
    epic = models.ForeignKey('epics.Epic', on_delete=models.CASCADE, related_name='task')

    def __str__(self):
        return self.title


class Bug(models.Model):

    title = models.CharField(max_length=64, default=' ', blank=False, unique=True)
    epic = models.ForeignKey('epics.Epic', on_delete=models.CASCADE, related_name='bug')

    def __str__(self):
        return self.title