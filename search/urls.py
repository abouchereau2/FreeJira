from django.urls import path
from .views import do_search

app_name = 'search'
urlpatterns = [
    #Bug search results
    path('', do_search, name='results')
]
