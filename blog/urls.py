from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogUpdateView, BlogDetailView, BlogDeleteView

appname = BlogConfig.name

urlpatterns = [
   path ('blog/', BlogListView.as_view(),name='blog_list'),
   path('new_blog/', BlogCreateView.as_view(), name='blog_create'),
   path('edit_blog/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
   path('view_blog/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
   path('delete_blog/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
]