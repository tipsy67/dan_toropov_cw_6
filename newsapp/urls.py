from django.urls import path

from newsapp.apps import NewsappConfig
from newsapp.views import NewsLetterListView, NewsLetterDetailView, change_status, ClientListView, MessageListView, \
    ClientUpdateView, MessageUpdateView, ClientCreateView, NewsLetterCreateView, MessageCreateView, NewsLetterUpdateView

app_name = NewsappConfig.name

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter_view/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_view'),
    path('newsletter_edit/<int:pk>', NewsLetterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter_new/', NewsLetterCreateView.as_view(), name='newsletter_new'),
    path('status/<int:pk>', change_status, name='status'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client_new/', ClientCreateView.as_view(), name='client_new'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('message_edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message_new/', MessageCreateView.as_view(), name='message_new'),

]