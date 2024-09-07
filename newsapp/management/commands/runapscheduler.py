from django.core.management.base import BaseCommand

from newsapp.src.newsapp_scheduler import NewsAppScheduler, NewsAppCommandScheduler

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        NewsAppCommandScheduler.start_scheduler()
