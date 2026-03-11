from django.apps import AppConfig
import sys


class CurrencyConfig(AppConfig):
    name = "apps.currency"
    
    def ready(self):
        if 'runserver' in sys.argv:
            from apps.currency.services import ExchangeRateService
            try:
                print("Filling db with initial data...")
                result = ExchangeRateService.sync_rates()
            except Exception as e:
                print(f"Could not perform startup sync: {e}")
