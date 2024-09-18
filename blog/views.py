from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from blog.models import Blog
from blog.utils import sendmail


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    template_name = '/blog/editor.html'
    extra_context = {
        'title_form': 'Добавить статью'
    }
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog/editor.html'
    extra_context = {
        'title_form': 'Изменить статью'
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
        if self.object.views_counter == 100:
            sendmail()
        return self.object
