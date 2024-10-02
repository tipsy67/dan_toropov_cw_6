
from django.contrib.auth.models import AbstractUser
from django.db import models
import random, string


NULLABLE = {'null':True, 'blank':True}

class User (AbstractUser):

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=30, **NULLABLE, verbose_name='телефон')
    token = models.CharField(max_length=100, **NULLABLE, verbose_name='токен')


    @staticmethod
    def generate_password(length: int):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))

        return password

    @property
    def is_manager(self):
        return True

    @property
    def is_content_manager(self):
        return self.has_perm('blog.can_edit_content')