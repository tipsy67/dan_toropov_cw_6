# Generated by Django 5.1 on 2024-08-25 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Тема')),
                ('text', models.TextField(verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('first_mailing_at', models.DateTimeField(verbose_name='Первая отправка')),
                ('periodic', models.CharField(choices=[('OT', 'Onetime'), ('PD', 'Daily'), ('PW', 'Weekly'), ('PM', 'Monthly')], default='OT', max_length=2, verbose_name='Переодичность')),
                ('status', models.CharField(choices=[('ON', 'active'), ('RUN', 'running'), ('OFF', 'inactive'), ('OK', 'completed')], default='OFF', max_length=3, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('clients', models.ManyToManyField(to='newsapp.client', verbose_name='Клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message', to='newsapp.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='NewsLetterHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Запущена')),
                ('finished_at', models.DateTimeField(verbose_name='Завершена')),
                ('is_success', models.BooleanField(verbose_name='Статус')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsapp.newsletter', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'История рассылок',
                'verbose_name_plural': 'История рассылок',
                'ordering': ['finished_at'],
            },
        ),
    ]
