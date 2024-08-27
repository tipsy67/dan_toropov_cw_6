from django.urls import path

from newsapp.apps import NewsappConfig
from newsapp.views import NewsLetterListView, NewsLetterDetailView, change_status, ClientListView, MessageListView, \
    ClientUpdateView, MessageUpdateView

app_name = NewsappConfig.name

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='home'),
    path('newsletter_view/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_view'),
    path('status/<int:pk>', change_status, name='status'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('message_edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),

]