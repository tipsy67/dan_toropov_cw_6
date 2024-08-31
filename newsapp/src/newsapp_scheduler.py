from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


def message_job():
    print("Запущен планировщик задач для запуска рассылок. Для остановки нажмите Ctrl+C")


class NewsAppCommandScheduler(BlockingScheduler):

    SCHEDULER:BackgroundScheduler|None = None

    def __init__(self):
        super().__init__(timezone=settings.TIME_ZONE)
        self.add_jobstore(DjangoJobStore(), "default")
        self.add_job(
            message_job,
            trigger=CronTrigger(second="*/10"),
            id="message_job_q2hd38",
            max_instances=1,
            replace_existing=True,
        )
        try:
            self.start()
        except KeyboardInterrupt:
            # self.shutdown(wait=False)
            # time.sleep(1)
            self.remove_job("message_job_q2hd38")



class NewsAppScheduler(BackgroundScheduler):

    SCHEDULER:BackgroundScheduler|None = None

    @classmethod
    def start_scheduler(cls):
        if cls.SCHEDULER is not None:
            cls.SCHEDULER = super().__init__(timezone=settings.TIME_ZONE)
            cls.SCHEDULER.add_jobstore(DjangoJobStore(), "default")
            cls.SCHEDULER.start()

    @classmethod
    def job_new(cls):
        pass

    @classmethod
    def job_on(cls, pk):
        pass

    @classmethod
    def job_off(cls, pk):
        pass

    @classmethod
    def job_update(cls, pk):
        pass

    @classmethod
    def job_delete(cls, pk):
        pass

    # The `close_old_connections` decorator ensures that database connections, that have become
    # unusable or are obsolete, are closed before and after your job has run. You should use it
    # to wrap any jobs that you schedule that access the Django database in any way.
    @util.close_old_connections
    def delete_old_job_executions(max_age=604_800):
        """
        This job deletes APScheduler job execution entries older than `max_age` from the database.
        It helps to prevent the database from filling up with old historical records that are no
        longer useful.

        :param max_age: The maximum length of time to retain historical job execution records.
                        Defaults to 7 days.
        """
        DjangoJobExecution.objects.delete_old_job_executions(max_age)

