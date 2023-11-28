include .env
LOCALES_PATH := ./data/locales
I18N_DOMAIN := $(or $(I18N_DOMAIN),bot)

run:
	./bin/entrypoint.sh
docker_run:
	docker-compose up -d
docker_logs: 
	docker-compose logs -f app
docker_rebuild: 
	docker-compose up -d --build --no-deps --force-recreate
mongosh: 
	docker-compose exec mongo mongosh
