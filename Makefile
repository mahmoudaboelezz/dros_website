install:
	pip install -r requirements.txt
freeze:
	pip list --format=freeze > requirements.txt
migrate:
	cd website && python manage.py migrate
run:
	cd website && python manage.py runserver 8090
makemigrations:
	cd website && python manage.py makemigrations
	cd website && python manage.py migrate
admin:
	cd website && python manage.py createsuperuser
format:
	black *.py website/*.py
lint:
	pylint --disable=R,C *.py website/*.py
build:
	docker compose build
up:
	docker-compose up -d
