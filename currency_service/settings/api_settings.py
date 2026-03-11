REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Currency Tracker API",
    "DESCRIPTION": "API for currency exchange rate tracking",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
