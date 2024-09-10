from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'
    verbose_name = 'Рассылки'

    def ready(self):
        import newsapp.signals
        from newsapp.src.newsapp_scheduler import NewsAppScheduler
        NewsAppScheduler.start_scheduler()
