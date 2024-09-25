from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog



class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Блог',
        'title_plural': 'статей'
    }

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    # template_name = 'blog/blog_form.html'
    extra_context = {
        'title': 'Блог',
        'title_card': 'Добавление статьи',
    }
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    # template_name = 'blog/blog_form.html'
    extra_context = {
        'title': 'Блог',
        'title_card': 'Редактирование статьи',
        'title_href': {'url': 'blog:blog_delete', 'text': 'Удалить статью'},
    }
    success_url = reverse_lazy('blog:blog_list')

    def get_success_url(self):
        return reverse('blog:blog_detail', args=(self.kwargs['slug'],))


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        # obj = get_object_or_404(Blog.objects,slug=self.kwargs[self.slug_url_kwarg])
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()

        return self.object

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Удаление статьи',
        'title_card': 'статьи',
        'title_href': {'url': 'blog:blog_update'},
    }
