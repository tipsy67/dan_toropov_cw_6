import secrets
from pyexpat.errors import messages

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView, ListView

from newsapp.src.utils import sendmail
from users.forms import ProfileUpdateForm, CreateUserForm, LoginUserForm
from users.models import User


class LoginView(BaseLoginView):
    form_class = LoginUserForm
    template_name = 'users/user_form.html'
    extra_context = {
        'title_form': 'Вход на сайт'
    }

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'recovery' in form.data:
            email = form.data.get('username')
            user = User.objects.filter(email=email).first()
            if user is not None:
                password = user.generate_password(8)
                user.password = make_password(password)
                user.save()
                sendmail(
                    [user.email],
                    'Восстановление пароля',
                    f'Ваш новый пароль {password}')
                messages.success(self.request, 'На вашу по4ту отправлен пароль')
                return redirect(reverse('users:login'))
            else:
                messages.warning(self.request, f'Пользователя {email} не существует')
        return super().form_invalid(form)


class UserListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    extra_context = {
        'title': 'Пользователи'
    }
    permission_required = 'users.view_user'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model =  get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'users/user_form.html'
    extra_context = {
        'title_form': 'Профиль пользователя'
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

class UserCreateView(CreateView):
    model = get_user_model()
    form_class = CreateUserForm
    template_name = 'users/user_form.html'
    extra_context = {
        'title_form': 'Регистрация пользователя',
        'create_user': True
    }
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.is_active = False
        user.token = token
        user.save()
        sendmail(
            [user.email],
            'Подтверждение регистрации',
        'Пожалуйста подтвердите свой адрес электронной почты для завершения регистрации\n'+
        f'http://{self.request.get_host()}/confirm/{token}')

        return super().form_valid(form)


def confirm_user(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse('users:login'))

@permission_required('users.can_change_status', raise_exception=True)
def change_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    elif not user.is_active == 'OFF':
        user.is_active = True
    user.save()
    return redirect(reverse('users:user_list'))