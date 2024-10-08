from django.db import models
from django.template.defaultfilters import truncatechars
from django_apscheduler.models import DjangoJobExecution

from users.models import User

NULLABLE = {'null':True, 'blank':True}

class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name ='Имя')
    last_name = models.CharField(max_length=50, verbose_name ='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name ='Отчество', **NULLABLE)
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, **NULLABLE,
                              related_name='clients', verbose_name='Владелец')

    def __str__(self):
        patronymic = ''
        if self.patronymic is not None:
            patronymic = self.patronymic
        return f'{self.last_name} {self.first_name} {patronymic}({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, **NULLABLE,
                              related_name='messages', verbose_name='Владелец')

    def __str__(self):
        return f'{self.title} ({truncatechars(self.text, 70)})'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class NewsLetter (models.Model):
    PEREODIC = {
        'OT': 'разовая',
        'PD': 'ежедневная',
        'PW': 'еженедельная',
        'PM': 'ежемесячная'
    }

    STATUS = {
        'ON': 'включена',
        'OFF': 'выключена',
    }

    name = models.CharField(max_length=50, verbose_name='Название')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    first_mailing_at = models.DateTimeField(verbose_name='Первая отправка')
    periodic = models.CharField(max_length=2, choices = PEREODIC, default='OT', verbose_name='Периодичность')
    status = models.CharField(max_length=3, choices= STATUS, default='OFF',  verbose_name='Статус')
    clients = models.ManyToManyField('Client', related_name='newsletters',verbose_name='Клиенты')
    message = models.ForeignKey('Message', on_delete=models.PROTECT, related_name='newsletters', verbose_name= 'Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= 'Создана')
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, **NULLABLE,
                                 related_name='products', verbose_name='Владелец')

    def __str__(self):
        return f'{self.name} ({self.first_mailing_at}) {self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['created_at', 'name']
        permissions = [
            ('can_change_status', 'Can change status')
        ]

    def get_history(self):
        return DjangoJobExecution.objects.filter(job_id=str(self.pk))
    # def save(self, *args,**kwargs):
    #     super(NewsLetter,self).save(*args, **kwargs)
    #     NewsAppScheduler.job_new(self)


class NewsLetterHistory (models.Model):

    newsletter = models.ForeignKey('NewsLetter', related_name='history', on_delete=models.CASCADE, verbose_name='Рассылка')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Запущена')
    finished_at = models.DateTimeField(verbose_name='Завершена')
    is_success = models.BooleanField(verbose_name='Статус')
    comment = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f'{self.newsletter} ({self.finished_at} - {self.is_success})'

    class Meta:
        verbose_name = 'История рассылок'
        verbose_name_plural = 'История рассылок'
        ordering = ['finished_at']