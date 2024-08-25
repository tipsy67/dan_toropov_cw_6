from django.urls import path

from newsapp.apps import NewsappConfig
from newsapp.views import NewsLetterListView, NewsLetterDetailView, change_status

app_name = NewsappConfig.name

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='home'),
    path('newsletter_view/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_view'),
    path('status/<int:pk>', change_status, name='status'),

]