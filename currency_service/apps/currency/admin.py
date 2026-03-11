from django.contrib import admin
from apps.currency.models import Currency, RateHistory


admin.site.register(Currency)
admin.site.register(RateHistory)