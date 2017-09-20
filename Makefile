WAIT = ./wait-for-it.sh localhost:5432 --timeout=60 --
COMPOSE_LOCAL = docker-compose -f docker-compose.local.yml
MANAGE = python src/manage.py
IMAGE_NAME = ghrecommender/ghrecommender

start_local_servers:
	$(COMPOSE_LOCAL) up -d redis postgres ghmodel mongodb
	$(WAIT)

stop_local_servers:
	$(COMPOSE_LOCAL) stop redis postgres ghmodel mongodb

collectstatic:
	$(MANAGE) collectstatic --noinput

migrate:
	$(MANAGE) migrate --noinput

test:
	DJANGO_CONFIGURATION=Test ./src/manage.py test

runserver:
	./src/manage.py runserver

build:
	docker build --tag=$(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)