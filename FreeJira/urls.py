from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from epics import urls as urls_epics
from search import urls as urls_search
from serialize import urls as urls_serialize
from home.views import index


urlpatterns = [
    #Admin interface
    path('admin/', admin.site.urls),
    #Home page
    path('', index, name='index'),
    #List of epics
    path('epics', include(urls_epics)),
    #Bug search results
    path('results', include(urls_search)),
    #Import/Export/Reset functions
    path('serialize', include(urls_serialize)),
]
