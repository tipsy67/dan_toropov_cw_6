from django import forms

from blog.models import Blog

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'is_published']


class BlogContentForm(BlogForm):

    def __init__(self, *args, **kwargs):
        super(BlogContentForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['content'].disabled = True
        self.fields['image'].disabled = True