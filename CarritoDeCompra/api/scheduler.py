from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
from api.utils import update_stock

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
scheduler.add_jobstore(DjangoJobStore(), "default")
job = scheduler.get_job("update_stock_job")

# If the job does not already exist, we add it to the scheduler
if job is None:
    scheduler.add_job(
        update_stock,
        trigger="cron",
        minute="0",  # This sets it to run at the start of every hour
        id="update_stock_job",  # Unique ID for this job
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
