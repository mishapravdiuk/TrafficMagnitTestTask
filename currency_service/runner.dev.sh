sleep 10
echo "Checking for migrations."
python manage.py migrate
echo "Migrations have already been made."

echo "Fetching initial currencies from API..."
python manage.py sync_currencies

echo "Starting server"
python manage.py runserver 0.0.0.0:8000