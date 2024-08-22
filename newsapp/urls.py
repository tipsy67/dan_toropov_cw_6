from django.urls import path

from newsapp.views import index

app_name = 'newsapp'

urlpatterns = [
    path('', index, name='home'),
]