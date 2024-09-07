from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from newsapp.src.utils import sendmail


class NewsAppCommandScheduler:
    """
    Класс для запуска планировщика из команды джанго.
    Блокирует дальнейшее выполнение до прерывания из консоли
    """

    SCHEDULER:BlockingScheduler|None = None

    @classmethod
    def start_scheduler(cls):
        cls.SCHEDULER = BlockingScheduler(timezone=settings.TIME_ZONE)
        cls.SCHEDULER.add_jobstore(DjangoJobStore(), "default")
        cls.SCHEDULER.add_job(
            cls.message_job,
            trigger=CronTrigger(second="*/10"),
            id="message_job_q2hd38",
            max_instances=1,
            replace_existing=True,
        )
        try:
            cls.SCHEDULER.start()
        except KeyboardInterrupt:
            # self.shutdown(wait=False)
            # time.sleep(1)
            cls.SCHEDULER.remove_job("message_job_q2hd38")

    @staticmethod
    def message_job():
        print("Запущен планировщик задач для запуска рассылок. Для остановки нажмите Ctrl+C")



class NewsAppScheduler:
    """
    Класс для работы с планировщиком из приложения рассылок
    """

    SCHEDULER:BackgroundScheduler|None = None

    @classmethod
    def start_scheduler(cls):
        if cls.SCHEDULER is None:
            cls.SCHEDULER = BackgroundScheduler(timezone=settings.TIME_ZONE)
            cls.SCHEDULER.add_jobstore(DjangoJobStore(), "default")
            cls.SCHEDULER.start()


    @classmethod
    def set_trigger_params(cls, obj):
        """
        Установка парметров триггера крон, исходя из свойств объекта NewsLetter
        """
        trigger_params = {'start_date': obj.first_mailing_at}
        obj_datetime = obj.first_mailing_at.timetuple()
        trigger_params['hour'] = obj_datetime.tm_hour
        trigger_params['minute'] = obj_datetime.tm_min
        if obj.periodic == 'PD':
            trigger_params['day'] = '*'
        elif obj.periodic == 'PW':
            trigger_params['day_of_week'] = obj_datetime.tm_wday
            trigger_params['week'] = '*'
        elif obj.periodic == 'PM':
            trigger_params['day'] = obj_datetime.tm_mday
            trigger_params['month'] = '*'
        else:
            trigger_params['day'] = obj_datetime.tm_mday
            trigger_params['month'] = obj_datetime.tm_mon
            trigger_params['year'] = '*'

        return trigger_params

    @classmethod
    def job_new(cls, obj):
        email_list = [x.email for x in obj.clients.all()]
        args = [email_list, obj.message.title, obj.message.text]
        cls.SCHEDULER.add_job(
            sendmail,
            trigger=CronTrigger(**cls.set_trigger_params(obj)),
            id=str(obj.pk),
            max_instances=1,
            replace_existing=True,
            args=args
        )

    @classmethod
    def job_on(cls, pk):
        cls.SCHEDULER.resume_job(str(pk))

    @classmethod
    def job_off(cls, pk):
        cls.SCHEDULER.pause_job(str(pk))

    @classmethod
    def job_update(cls, obj):
        cls.SCHEDULER.reschedule_job(
            trigger=CronTrigger(**cls.set_trigger_params(obj)),
            job_id=obj.pk
        )

    @classmethod
    def job_delete(cls, pk):
        cls.SCHEDULER.remove_job(str(pk))

    # The `close_old_connections` decorator ensures that database connections, that have become
    # unusable or are obsolete, are closed before and after your job has run. You should use it
    # to wrap any jobs that you schedule that access the Django database in any way.
    @util.close_old_connections
    def delete_old_job_executions(self, max_age=604_800):
        """
        This job deletes APScheduler job execution entries older than `max_age` from the database.
        It helps to prevent the database from filling up with old historical records that are no
        longer useful.

        :param max_age: The maximum length of time to retain historical job execution records.
                        Defaults to 7 days.
        """
        DjangoJobExecution.objects.delete_old_job_executions(max_age)

