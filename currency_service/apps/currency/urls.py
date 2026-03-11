from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.currency.views import CurrencyViewSet

router = SimpleRouter()
router.register(r"currencies", CurrencyViewSet, basename="currency")

urlpatterns = [
    path("", include(router.urls)),
]
