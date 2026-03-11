import httpx
import pycountry
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.currency.models import Currency, RateHistory

class ExchangeRateService:
    UAH_CODE = 980

    @classmethod
    def sync_rates(cls):
        external_data = cls._fetch_external_data()
        if not external_data:
            return "No data fetched"

        filtered_data = cls._filter_uah_pairs(external_data)
        
        with transaction.atomic():
            cls._ensure_currencies_exist(filtered_data)
            records_created = cls._save_rate_history(filtered_data)

        return f"Sync complete. Recorded {records_created} new rates."

    @classmethod
    def _fetch_external_data(cls):
        """Отримання даних із зовнішнього API"""
        try:
            with httpx.Client(http2=True, timeout=10.0) as client:
                response = client.get(settings.CURRENCY_API_URL)
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError):
            return None

    @classmethod
    def _filter_uah_pairs(cls, data):
        return [
            item for item in data 
            if item.get('currencyCodeB') == cls.UAH_CODE
        ]

    @classmethod
    def _ensure_currencies_exist(cls, data):
        incoming_codes = {item['currencyCodeA'] for item in data}
        existing_codes = set(Currency.objects.filter(
            code__in=incoming_codes
        ).values_list('code', flat=True))

        new_codes = incoming_codes - existing_codes
        
        if new_codes:
            new_currencies = []
            for code in new_codes:
                currency_info = pycountry.currencies.get(numeric=str(code).zfill(3))
                iso_code = currency_info.alpha_3 if currency_info else str(code)
                name = currency_info.name if currency_info else f"Currency {code}"

                new_currencies.append(
                    Currency(
                        code=code,
                        iso_code=iso_code,
                        name=name,
                        is_monitored=False
                    )
                )
            Currency.objects.bulk_create(new_currencies)

    @classmethod
    def _save_rate_history(cls, data):
        monitored_currencies = {
            c.code: c for c in Currency.objects.filter(is_monitored=True)
        }
        
        history_records = []
        for item in data:
            code = item['currencyCodeA']
            if code in monitored_currencies:
                history_records.append(
                    RateHistory(
                        currency=monitored_currencies[code],
                        buy_rate=item.get('rateBuy') or item.get('rateCross'),
                        sell_rate=item.get('rateSell') or item.get('rateCross'),
                        added_at=timezone.now()
                    )
                )

        if history_records:
            RateHistory.objects.bulk_create(history_records)
        
        return len(history_records)