from django.db import models


class Currency(models.Model):
    code = models.PositiveIntegerField(unique=True, help_text="ISO 4217 numeric code")
    iso_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, blank=True)
    is_monitored = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name_plural = "currencies"
        db_table = "Currencies"
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.iso_code} ({self.code})"


class RateHistory(models.Model):
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="rates"
    )
    buy_rate = models.DecimalField(max_digits=12, decimal_places=4)
    sell_rate = models.DecimalField(max_digits=12, decimal_places=4)
    added_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-added_at"]
        verbose_name = "Rate History"
        verbose_name_plural = "Rate Histories"

    def __str__(self):
        return f"{self.currency.iso_code} at {self.added_at}"
