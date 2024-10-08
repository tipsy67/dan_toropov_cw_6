# Generated by Django 5.1 on 2024-08-27 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_alter_newsletter_options_newsletterhistory_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Изменено'),
        ),
        migrations.AlterField(
            model_name='newsletterhistory',
            name='newsletter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='newsapp.newsletter', verbose_name='Рассылка'),
        ),
    ]
