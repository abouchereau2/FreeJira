from django.urls import path
from .views import *

app_name = 'serialize'
urlpatterns = [
    #Import backlog
    path('import', simple_upload, name='import'),
    #Export backlog
    path('export', export, name='export'),
    #Reset database
    path('reset', reset, name='reset'),
]
