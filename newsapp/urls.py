from django.urls import path

from newsapp.apps import NewsappConfig
from newsapp.views import NewsLetterListView, NewsLetterDetailView, change_status, ClientListView, MessageListView, \
    ClientUpdateView, MessageUpdateView, ClientCreateView, NewsLetterCreateView, MessageCreateView, \
    NewsLetterUpdateView, MessageDeleteView, NewsLetterDeleteView, ClientDeleteView, mainpage

app_name = NewsappConfig.name

urlpatterns = [
    path('', mainpage, name='home'),
    path('newsletter_list', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter_view/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_view'),
    path('newsletter_edit/<int:pk>', NewsLetterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter_delete/<int:pk>', NewsLetterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter_new/', NewsLetterCreateView.as_view(), name='newsletter_new'),
    path('status/<int:pk>', change_status, name='status'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client_new/', ClientCreateView.as_view(), name='client_new'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('message_edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('message_new/', MessageCreateView.as_view(), name='message_new'),

]