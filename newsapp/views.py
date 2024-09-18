from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from newsapp.forms import NewsLetterForm
from newsapp.models import NewsLetter, Client, Message
from newsapp.src.newsapp_scheduler import NewsAppScheduler


# Рассылки ------------------------
class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'newsapp/newsletter_list.html'
    extra_context = {
        'title': 'Рассылки'
    }


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:newsletter_list')
    extra_context = {
        'title': 'Рассылка',
        'title_card': 'Редактирование рассылки',
        'title_href': {'url': 'newsapp:newsletter_delete', 'text': 'Удалить рассылку'},
    }

    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save()
            new_obj.status = 'OFF'
            new_obj.save()
            NewsAppScheduler.job_new(new_obj)
            NewsAppScheduler.job_off(new_obj.pk)

        return super().form_valid(form)


class NewsLetterCreateView(CreateView):
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
            NewsAppScheduler.job_new(new_obj)
            NewsAppScheduler.job_off(new_obj.pk)

        return super().form_valid(form)


class NewsLetterDetailView(DetailView):
    model = NewsLetter


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:newsletter_list')
    extra_context = {
        'title': 'Удаление рассылки',
        'title_card': 'рассылку',
        'title_href': {'url': 'newsapp:newsletter_edit'},
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        NewsAppScheduler.job_delete(self.object.pk)
        super(NewsLetterDeleteView,self).delete(*args, **kwargs)

# Клиенты ------------------------
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
        'title_card': 'Редактирование клиента',
        'title_href': {'url': 'newsapp:client_delete', 'text': 'Удалить клиента'},
    }


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Удаление клиента',
        'title_card': 'клиента',
        'title_href': {'url': 'newsapp:client_edit'},
    }


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:client_list')
    extra_context = {
        'title': 'Клиент',
        'title_card': 'Добавление клиента',
    }


# Сообщения ------------------------
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
        'title_href': {'url': 'newsapp:message_delete', 'text': 'Удалить сообщениe'},
        'title_card': 'Редактирование сообщения'
    }


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsapp/uni_delete.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Удаление сообщения',
        'title_card': 'сообщение',
        'title_href': {'url': 'newsapp:message_edit'},
    }


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    template_name = 'newsapp/uni_edit.html'
    success_url = reverse_lazy('newsapp:message_list')
    extra_context = {
        'title': 'Сообщениe',
        'title_card': 'Добавление сообщения',
    }


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
    return render(request, 'newsapp/index.html')