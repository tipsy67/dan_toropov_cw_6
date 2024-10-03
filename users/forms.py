from cProfile import label

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class LoginUserForm(AuthenticationForm):
    username = UsernameField(label= 'Логин', widget=forms.TextInput(attrs={"autofocus": True}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ProfileUpdateForm(forms.ModelForm):

    username = forms.CharField(label= 'Логин', disabled=True)
    email = forms.EmailField(disabled=True)

    class Meta:
        model = get_user_model()
        fields =('username', 'email', 'first_name', 'last_name', 'phone', 'avatar')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields =('username', 'email', 'first_name', 'last_name', 'password1', 'password2')