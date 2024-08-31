from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand

from newsapp.src.newsapp_scheduler import NewsAppScheduler, NewsAppCommandScheduler


def my_job():
    # Your job processing logic here...
    print('ok ')



class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = NewsAppCommandScheduler()
