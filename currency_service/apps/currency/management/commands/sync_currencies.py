from django.core.management.base import BaseCommand
from apps.currency.services import ExchangeRateService

class Command(BaseCommand):
    help = 'Sync currency data with Monobank API'

    def handle(self, *args, **options):
        self.stdout.write("Starting synchronization with Monobank")
        try:
            result = ExchangeRateService.sync_rates()
            self.stdout.write(self.style.SUCCESS(f"Successfully finished: {result}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Sync failed: {str(e)}"))
            