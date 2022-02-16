from django.test import TestCase, Client
from django.urls import reverse

from epics.models import Epic, Bug, Task
from epics.tests import create_Epic, create_Bug, create_Task


class TestSearchView(TestCase):

    """
    Test search view
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        '''
        Creates a test case:
        Epic1
        |_Epic2
          |_Epic3 -> Bug

        For 'bug' search word, results should be in order: Epic1, Epic2, Epic3
        '''
        self.e1 = create_Epic('Epic1', None)
        self.e2 = create_Epic('Epic2', self.e1)
        self.e3 = create_Epic('Epic3', self.e2)
        self.bug = create_Bug('Bug', self.e3)
        self.e3.refresh_status()
        self.e2.refresh_status()
        self.e1.refresh_status()

    '''
    Test the results view
    '''
    def test_search_results_get(self):
        response = self.client.get(reverse('search:results') + '?q=Bug')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bugs'][self.bug.title]), 3)

        for idx, epic in enumerate(response.context['bugs'][self.bug.title]):
            if idx == 0: self.assertEqual(epic, self.e1)
            if idx == 1: self.assertEqual(epic, self.e2)
            if idx == 2: self.assertEqual(epic, self.e3)

    '''
    Test result view when no results
    '''
    def test_search_empty_get(self):
        response = self.client.get(reverse('search:results') + '?q=nobughere')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bugs']), 0)



