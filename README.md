# Currency Tracker Service

Сервіс для відстеження курсів валют відносно гривні за допомогою API Monobank.

## Стек технологій
- Python 3.12 / Django 6
- PostgreSQL
- Redis + Celery
- Poetry
- DRF

# Процес запуску
1. Завантажити репозиторій
```bash
git clone https://github.com/mishapravdiuk/TrafficMagnitTestTask.git
```
2. Перейти до каталогу
```bash
cd TrafficMagnitTestTask
```
4. Створити конфіг файл
```bash 
mkdir -p currency_service/configs && cat <<EOF > currency_service/configs/file.env
POSTGRES_DB=currency_service_db
POSTGRES_USER=currency_service_user
POSTGRES_PASS=KtfLQeQIDIuTppbWLQ
POSTGRES_PORT=5432
POSTGRES_HOST=postgres
SECRET_KEY=django-insecure-0&u1f-su3b%$n^n5oo_j-uwzk!iv^6#!g(95rg7$6uvuqrzlo8
DEBUG=True
CURRENCY_API_URL=https://api.monobank.ua/bank/currency
REDIS_PORT=6379
REDIS_HOST=host.docker.internal
REDIS_CACHE_DB=0
EOF
```
5. Запустити docker engine
6. Забілдити збірку
```bash 
docker compose -f docker-compose.dev.yaml build
```
6. Підняти контейнер 
```bash 
docker compose -f docker-compose.dev.yaml up -d 
```
7. Перейти по посиланню 
```bash 
http://127.0.0.1:58000/api/docs/#/
```
