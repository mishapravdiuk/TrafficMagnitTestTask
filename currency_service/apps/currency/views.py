from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date

from apps.currency.models import Currency
from apps.currency.serializers import CurrencySerializer, RateHistorySerializer


class CurrencyViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.filter(is_monitored=True)

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        available_currencies = Currency.objects.filter(is_monitored=False)
        serializer = self.get_serializer(available_currencies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='track')
    def track(self, request, code=None):
        currency = self.get_object()
        currency.is_monitored = True
        currency.save()
        return Response({'status': f'Currency {currency.iso_code} is now monitored'})
    

    @action(detail=True, methods=['patch'], url_path='toggle')
    def toggle_monitoring(self, request, code=None):
        currency = self.get_object()
        currency.is_monitored = not currency.is_monitored
        currency.save()
        state = "on" if currency.is_monitored else "off"
        return Response({'status': f'Monitoring for {currency.iso_code} turned {state}'})

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, code=None):
        currency = self.get_object()
        
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        rates = currency.rates.all()

        if start_date:
            rates = rates.filter(added_at__date__gte=parse_date(start_date))
        if end_date:
            rates = rates.filter(added_at__date__lte=parse_date(end_date))

        serializer = RateHistorySerializer(rates, many=True)
        return Response(serializer.data)
