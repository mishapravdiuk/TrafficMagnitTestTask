echo "Checking for migrations."
python manage.py migrate
echo "Migrations have already been made."

echo "Starting server"
python manage.py runserver 0.0.0.0:8000