import csv

from django.core.management.base import BaseCommand

from apps.currency.models import Currency


class Command(BaseCommand):
    help = "Export actual rates into csv file"

    def handle(self, *args, **options):
        filename = "current_rates.csv"

        currencies = Currency.objects.filter(is_monitored=True)

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ISO Code", "Name", "Buy Rate", "Sell Rate", "Updated At"])

            for currency in currencies:
                last_rate = currency.rates.order_by("-added_at").first()

                if last_rate:
                    writer.writerow(
                        [
                            currency.iso_code,
                            currency.name,
                            last_rate.buy_rate,
                            last_rate.sell_rate,
                            last_rate.added_at.strftime("%Y-%m-%d %H:%M:%S"),
                        ]
                    )

        self.stdout.write(self.style.SUCCESS(f"File {filename} created successfully!"))
