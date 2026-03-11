from rest_framework import serializers

from apps.currency.models import Currency, RateHistory


class RateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RateHistory
        fields = ["buy_rate", "sell_rate", "added_at"]


class CurrencySerializer(serializers.ModelSerializer):
    current_rate = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ["id", "code", "iso_code", "name", "is_monitored", "current_rate"]

    def get_current_rate(self, obj):
        last_rate = obj.rates.first()
        if last_rate:
            return RateHistorySerializer(last_rate).data
        return None
