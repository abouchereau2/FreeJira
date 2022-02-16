from django.test import TestCase, Client
from django.urls import reverse

from .models import Epic, Bug, Task


'''
Utility functions for testing
'''
def create_Epic(name, linked_epic):
    return Epic.objects.create(title=name, linked_epic=linked_epic)

def create_Bug(name, linked_epic):
    return Bug.objects.create(title=name, epic=linked_epic)

def create_Task(name, linked_epic):
    return Task.objects.create(title=name, epic=linked_epic)


'''
Test the epic model
'''
class TestEpicModel(TestCase):

    #Test of refresh_status
    def test_state(self):
        e1 = create_Epic('EpicA', None)
        e2 = create_Epic('EpicB', e1)
        e3 = create_Epic('EpicC', None)
        e4 = create_Epic('EpicD', e3)
        e5 = create_Epic('EpicE', None)

        b1 = create_Bug('BugB1', e2)
        b2 = create_Bug('BugE1', e5)

        t1 = create_Task('TaskA1', e1)
        t2 = create_Task('TaskA2', e1)
        t3 = create_Task('TaskB1', e2)
        t4 = create_Task('TaskB2', e2)

        e2.refresh_status()
        e1.refresh_status()
        e3.refresh_status()
        e4.refresh_status()
        e5.refresh_status()

        self.assertIs(e1.state, 'in_progress')
        self.assertIs(e2.state, 'in_progress')
        self.assertIs(e3.state, 'completed')
        self.assertIs(e4.state, 'completed')
        self.assertIs(e5.state, 'pending')


    #test of recursive function get_linked_bugs
    def test_get_linked_bugs(self):
        e1 = create_Epic('EpicA', None)
        e2 = create_Epic('EpicB', e1)
        b1 = create_Bug('BugB1', e2)
        self.assertEqual(len(e1.get_linked_bugs()), 1)

        b2 = create_Bug('BugB2', e2)
        self.assertEqual(len(e1.get_linked_bugs()), 2)

        e3 = create_Epic('EpicC', e2)
        b3 = create_Bug('BugC1', e3)
        self.assertEqual(len(e1.get_linked_bugs()), 3)



class TestEpicViews(TestCase):

    """
    Test epic views
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.obj = create_Epic('Epic1', None)
        self.bug = create_Bug('Bug1', self.obj)
        self.task = create_Task('Task1', self.obj)
        self.linked_epic = create_Epic('Epic2', self.obj)
        self.linked_bug = create_Bug('Bug2', self.linked_epic)

    #Test epics view list
    def test_epics_list_get(self):
        response = self.client.get(reverse('epics:epics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['epics'].count(), 2)

    #Test epic detailed view
    def test_epic_details_get(self):
        response = self.client.get(reverse('epics:epic', args=[self.obj.pk,]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['epic'], self.obj)
        self.assertEqual(response.context['bugs'].first(), self.bug)
        self.assertEqual(response.context['tasks'].first(), self.task)
        self.assertEqual(response.context['linked_epics'].first(), self.linked_epic)
        self.assertEqual(response.context['linked_bugs'][0], self.linked_bug.title)

    #Test add a bug form
    def test_epic_add_bug_post(self):
        response = self.client.post(reverse('epics:add_bug', args=[self.obj.pk,]), {
            'title': 'new bug'
        })

        self.assertTrue(Bug.objects.get(title='new bug'))
        self.assertEqual(Bug.objects.filter(epic=self.obj).count(), 2)

    #Test add a task form
    def test_epic_add_task_post(self):
        response = self.client.post(reverse('epics:add_task', args=[self.obj.pk,]), {
            'title': 'new task'
        })

        self.assertTrue(Task.objects.get(title='new task'))
        self.assertEqual(Task.objects.filter(epic=self.obj).count(), 2)

    #Test delete a bug
    def test_epic_del_bug_post(self):
        response = self.client.post(reverse('epics:delete_bug', args=[self.obj.pk, self.bug.pk]))

        self.assertFalse(Bug.objects.filter(pk=self.bug.pk))
        self.assertEqual(Bug.objects.filter(epic=self.obj).count(), 0)

    #Test delete a task
    def test_epic_del_task_post(self):
        response = self.client.post(reverse('epics:delete_task', args=[self.obj.pk, self.task.pk]))

        self.assertFalse(Task.objects.filter(pk=self.task.pk))
        self.assertEqual(Task.objects.filter(epic=self.obj).count(), 0)