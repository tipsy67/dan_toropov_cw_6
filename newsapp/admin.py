from django.contrib import admin

from newsapp.models import NewsLetter, Client, Message, NewsLetterHistory


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_filter = ('name', 'message', 'status')
    fields = ('name', 'first_mailing_at', 'periodic', 'status', 'message', 'clients')
    list_display = ('pk', 'name',  'first_mailing_at', 'status', )
    list_display_links = ('name',)
    filter_horizontal = ['clients']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'last_name', 'email')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_filter = ('title', 'created_at')

@admin.register(NewsLetterHistory)
class NewsLetterHistoryAdmin(admin.ModelAdmin):
    list_filter = ('newsletter', 'is_success')

