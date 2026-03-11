import os


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", default="redis://redis:6379/0"
)

CELERY_BEAT_SCHEDULE = {
    "update-rates-every-5-minutes": {
        "task": "sync_monobank_rates",
        "schedule": 300.0,
    },
}
