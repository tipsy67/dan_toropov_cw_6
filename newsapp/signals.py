from idlelib.debugobj import dispatch

from django.db.models.signals import pre_delete, post_save, post_delete
from django.dispatch import receiver

from newsapp.models import NewsLetter
from newsapp.src.newsapp_scheduler import NewsAppScheduler


@receiver(post_delete, sender=NewsLetter, weak=False, dispatch_uid='delete_job')
def delete_job(sender, instance, using, **kwargs):
    NewsAppScheduler.job_delete(instance.pk)