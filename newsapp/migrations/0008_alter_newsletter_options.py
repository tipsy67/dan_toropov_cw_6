# Generated by Django 5.1 on 2024-10-03 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0007_client_owner_message_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'ordering': ['created_at', 'name'], 'permissions': [('can_change_status', 'Can change status')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
