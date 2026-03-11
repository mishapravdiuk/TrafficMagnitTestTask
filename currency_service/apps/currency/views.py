from apps.currency.models import Currency
from apps.currency.serializers import CurrencySerializer, RateHistorySerializer
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CurrencyViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_queryset(self):
        if self.action == "list":
            return Currency.objects.filter(is_monitored=True)

        return Currency.objects.all()

    @action(detail=False, methods=["get"], url_path="available")
    def available(self, request):
        available_currencies = Currency.objects.filter(is_monitored=False)
        serializer = self.get_serializer(available_currencies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path=r"track/(?P<code>[^/.]+)")
    def track(self, request, code=None):
        currency = get_object_or_404(Currency.objects.all(), code=code)

        if currency.is_monitored:
            return Response(
                {"detail": "Already monitored"}, status=status.HTTP_400_BAD_REQUEST
            )

        currency.is_monitored = True
        currency.save(update_fields=["is_monitored"])

        return Response({"status": f"Currency {currency.code} added to monitoring"})

    @action(detail=True, methods=["patch"], url_path="toggle")
    def toggle_monitoring(self, request, pk=None):
        currency = get_object_or_404(Currency, code=pk)
        currency.is_monitored = not currency.is_monitored
        currency.save(update_fields=["is_monitored"])

        state = "on" if currency.is_monitored else "off"
        return Response(
            {"status": f"Monitoring for {currency.iso_code} turned {state}"}
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start", description="Start date (YYYY-MM-DD)", type=str
            ),
            OpenApiParameter(name="end", description="End date (YYYY-MM-DD)", type=str),
        ]
    )
    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        currency = get_object_or_404(Currency, code=pk)

        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")

        rates = currency.rates.all().order_by("-added_at")

        if start_date:
            parsed_start = parse_date(start_date)
            if parsed_start:
                rates = rates.filter(added_at__date__gte=parsed_start)

        if end_date:
            parsed_end = parse_date(end_date)
            if parsed_end:
                rates = rates.filter(added_at__date__lte=parsed_end)

        serializer = RateHistorySerializer(rates, many=True)
        return Response(serializer.data)
