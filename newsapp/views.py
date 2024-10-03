import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from blog.models import Blog
from newsapp.forms import NewsLetterForm
from newsapp.models import NewsLetter, Client, Message
from newsapp.src.newsapp_scheduler import NewsAppScheduler


# Рассылки ------------------------
class NewsLetterListView(LoginRequiredMixin, ListView):
    model = NewsLetter
    template_name = 'newsapp/newsletter_list.html'
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        if self.request.user.has_perm('newsapp.view_newsletter'):
            return NewsLetter.objects.all()

        return NewsLetter.objects.filter(owner=self.request.user)


class NewsLetterUpdateView(UserPassesTestMixin, UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:newsletter_list')
    extra_context = {
        'title': 'Рассылка',
        'title_card': 'Редактирование рассылки',
        'title_href': {'url': 'newsapp:newsletter_delete', 'text': 'Удалить рассылку'},
    }


    def test_func(self):
        return self.request.user.has_perm('newsapp.change_newsletter') or self.request.user == self.get_object().owner


    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save()
            new_obj.status = 'OFF'
            new_obj.save()
            NewsAppScheduler.job_new(new_obj)
            NewsAppScheduler.job_off(new_obj.pk)

        return super().form_valid(form)


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:newsletter_list')
    extra_context = {
        'title': 'Рассылка',
        'title_card': 'Добавление рассылки',
    }


    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save()
            new_obj.owner = self.request.user
            new_obj.save()
            NewsAppScheduler.job_new(new_obj)
            NewsAppScheduler.job_off(new_obj.pk)

        return super().form_valid(form)


class NewsLetterDetailView(UserPassesTestMixin, DetailView):
    model = NewsLetter


    def test_func(self):
        return self.request.user.has_perm('newsapp.view_newsletter') or self.request.user == self.get_object().owner


class NewsLetterDeleteView(UserPassesTestMixin, DeleteView):
    model = NewsLetter
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:newsletter_list')
    extra_context = {
        'title': 'Удаление рассылки',
        'title_card': 'рассылку',
        'title_href': {'url': 'newsapp:newsletter_edit'},
    }


    def test_func(self):
        return self.request.user.has_perm('newsapp.delete_newsletter') or self.request.user == self.get_object().owner


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        NewsAppScheduler.job_delete(self.object.pk)
        super(NewsLetterDeleteView,self).delete(*args, **kwargs)

# Клиенты ------------------------
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    # template_name = 'newsapp/other_list.html'
    extra_context = {
        'title': 'Клиенты',
        'title_plural': 'клиентов'
    }

    def get_queryset(self):
        if self.request.user.has_perm('newsapp.view_client'):
            return Client.objects.all()

        return Client.objects.filter(owner=self.request.user)


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'patronymic', 'email', 'comment']
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Клиент',
        'title_card': 'Редактирование клиента',
        'title_href': {'url': 'newsapp:client_delete', 'text': 'Удалить клиента'},
    }


    def test_func(self):
        return self.request.user.has_perm('newsapp.change_client') or self.request.user == self.get_object().owner



class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Удаление клиента',
        'title_card': 'клиента',
        'title_href': {'url': 'newsapp:client_edit'},
    }


    def test_func(self):
        return self.request.user.has_perm('newsapp.delete_client') or self.request.user == self.get_object().owner


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Клиент',
        'title_card': 'Добавление клиента',
    }

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.owner = self.request.user
            client.save()
        return super().form_valid(form)

# Сообщения ------------------------
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения',
        'title_plural': 'сообщений'
    }


    def get_queryset(self):
        if self.request.user.has_perm('newsapp.view_message'):
            return Message.objects.all()

        return Message.objects.filter(owner=self.request.user)


class MessageUpdateView(UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('title', 'text')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Сообщениe',
        'title_href': {'url': 'newsapp:message_delete', 'text': 'Удалить сообщениe'},
        'title_card': 'Редактирование сообщения'
    }


    def test_func(self):
        return self.request.user.has_perm('newsapp.change_message') or self.request.user == self.get_object().owner


class MessageDeleteView(UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Удаление сообщения',
        'title_card': 'сообщение',
        'title_href': {'url': 'newsapp:message_edit'},
    }

    def test_func(self):
        return self.request.user.has_perm('newsapp.delete_message') or self.request.user == self.get_object().owner


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('title', 'text')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Сообщениe',
        'title_card': 'Добавление сообщения',
    }


    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.owner = self.request.user
            message.save()
        return super().form_valid(form)


@login_required
def change_status(request, pk):
    page = request.GET['page']
    newsletter_item = get_object_or_404(NewsLetter, pk=pk)
    if newsletter_item.status == 'ON':
        newsletter_item.status = 'OFF'
        NewsAppScheduler.job_off(pk)
    elif newsletter_item.status == 'OFF':
        newsletter_item.status = 'ON'
        NewsAppScheduler.job_on(pk)
    newsletter_item.save()
    if page == 'detail':
        return redirect(reverse('newsapp:newsletter_view', args=(pk,)))
    return redirect(reverse('newsapp:newsletter_list'))


def mainpage(request):

    blog_set = Blog.objects.filter(is_published=True).order_by('?')
    object_list = blog_set[:3]

    active_newsletter = NewsLetter.objects.filter(status='ON').count()
    disable_newsletter = NewsLetter.objects.filter(status='OFF').count()
    total_newsletter = NewsLetter.objects.count()

    total_clients = Client.objects.values('email').distinct().count()

    context = {
        "data_set": [disable_newsletter, active_newsletter],
        "total_newsletter": total_newsletter,
        "object_list": object_list,
        "total_clients": total_clients
    }
    return render(request, 'newsapp/index.html', context)