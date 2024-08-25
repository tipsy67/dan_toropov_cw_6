

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from newsapp.models import NewsLetter


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'newsapp/index.html'
    extra_context = {
        'title': 'Рассылки'
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





