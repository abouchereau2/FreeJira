from django.test import TestCase

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
class EpicModelTest(TestCase):

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

        with self.subTest():
            self.assertIs(e1.state, 'in_progress')
        with self.subTest():
            self.assertIs(e2.state, 'in_progress')
        with self.subTest():
            self.assertIs(e3.state, 'completed')
        with self.subTest():
            self.assertIs(e4.state, 'completed')
        with self.subTest():
            self.assertIs(e5.state, 'pending')


    #test of recursive function get_linked_bugs
    def test_get_linked_bugs(self):
        e1 = create_Epic('EpicA', None)
        e2 = create_Epic('EpicB', e1)
        b1 = create_Bug('BugB1', e2)

        with self.subTest():
            self.assertEqual(len(e1.get_linked_bugs()), 1)

        b2 = create_Bug('BugB2', e2)

        with self.subTest():
            self.assertEqual(len(e1.get_linked_bugs()), 2)

        e3 = create_Epic('EpicC', e2)
        b3 = create_Bug('BugC1', e3)

        with self.subTest():
            self.assertEqual(len(e1.get_linked_bugs()), 3)
