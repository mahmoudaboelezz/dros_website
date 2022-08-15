install:
	pip install -r requirements.txt
	poetry install
freeze:
	pip list --format=freeze > requirements.txt
migrate:
	cd website && python manage.py migrate
run:
	cd website && python manage.py runserver
makemigrations:
	cd website && python manage.py makemigrations
	cd website && python manage.py migrate
admin:
	cd website && python manage.py createsuperuser
format:
	black *.py mylib/*.py
lint:
	pylint --disable=R,C *.py mylib/*.py
build:
	docker compose build
up:
	docker-compose up -d
