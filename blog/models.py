import random

from django.db import models
from django.template.defaultfilters import truncatechars
from pytils.translit import slugify

from users.models import User, NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_counter = models.IntegerField(default=0, verbose_name='Количество просмотров')
    content = models.TextField(verbose_name='Содержимое')
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, **NULLABLE,
                                 related_name='blogs', verbose_name='Владелец')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
        permissions = [
            ('can_publish_article' , 'Can publish article')
        ]

    def __str__(self):
        return f'{self.title}'

    @property
    def short_content(self):
        return truncatechars(self.content, 100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super(Blog,self).save(*args, **kwargs)

