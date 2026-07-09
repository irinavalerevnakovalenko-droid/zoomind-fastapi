from celery import Celery

from app.core.config import settings

celery_app = Celery(
    'zoomind',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        'app.tasks.debug',
        'app.tasks.orders',
    ],
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'send-repeat-purchase-reminders-daily': {
            'task': 'orders.send_repeat_purchase_reminders',
            'schedule': 60 * 60 * 24,
        },
    },
)

