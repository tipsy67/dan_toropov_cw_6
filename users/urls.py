from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UserConfig
from users.views import LoginView, ProfileUpdateView, UserCreateView, confirm_user

appname = UserConfig.name

urlpatterns = [
   path ('login/', LoginView.as_view(), name='login'),
   path ('logout/', LogoutView.as_view(), name='logout'),
   path('profile/', ProfileUpdateView.as_view(), name='profile'),
   path('register/', UserCreateView.as_view(), name='register'),
   path('confirm/<str:token>', confirm_user, name='confirm'),
]