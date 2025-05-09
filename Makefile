.PHONY: test dev docker-build docker-compose-up docker-compose-down

VERSION := 0.1.0
IMAGE_NAME := releads-docker:$(VERSION)

test:
	@env poetry run pytest -s -vv

dev:
	@env poetry run gunicorn -k uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:8888 -w 4 app.main:app

docker-build:
	@docker build -t $(IMAGE_NAME) .

docker-compose-up:
	@docker-compose up -d --build --remove-orphans --force-recreate

docker-compose-down:
	@docker-compose down -v --remove-orphans --rmi all
	@docker-compose rm -f -v 

docker-compose-update:
	@docker-compose down -v --remove-orphans --rmi all
	@docker-compose rm -f -v 
	@docker-compose up -d --build --remove-orphans --force-recreate
