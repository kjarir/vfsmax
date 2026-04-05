from celery import Celery
from app.core import config

celery_app = Celery(
    "vfsmax-worker",
    broker=config.settings.CELERY_BROKER_URL,
    backend=config.settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3000,
    worker_concurrency=config.settings.MAX_CONCURRENT_WORKERS,
)

# Auto-discover tasks from app.tasks
celery_app.autodiscover_tasks(["app.tasks"])


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
