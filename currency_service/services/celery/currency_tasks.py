from celery import shared_task

from apps.currency.services import ExchangeRateService


@shared_task(name="sync_monobank_rates")
def sync_rates_task():
    return ExchangeRateService.sync_rates()
