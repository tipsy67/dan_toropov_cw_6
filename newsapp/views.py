import os.path

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from newsapp.admin import ClientAdmin
from newsapp.models import NewsLetter, Client, Message


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'newsapp/index.html'
    extra_context = {
        'title': 'Рассылки'
    }

class ClientListView(ListView):
    model = Client
    # template_name = 'newsapp/other_list.html'
    extra_context = {
        'title': 'Клиенты',
        'title_plural': 'клиентов'
    }

class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Клиент',
        'title_card': 'Редактирование клиента'
    }

class MessageListView(ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения',
        'title_plural': 'сообщений'
    }

class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Сообщениe',
        'title_card': 'Редактирование сообщения'
    }


class NewsLetterDetailView(DetailView):
    model = NewsLetter


def change_status(request, pk):
    newsletter_item = get_object_or_404(NewsLetter, pk=pk)
    if newsletter_item.status == 'ON':
        newsletter_item.status = 'OFF'
    elif newsletter_item.status == 'OFF':
        newsletter_item.status = 'ON'
    newsletter_item.save()

    return redirect(reverse('newsapp:home'))





