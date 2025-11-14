build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

selecciondocente-config:
	docker compose -f local.yml config

makemigrations:
	docker compose -f local.yml run --rm app python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm app python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm app python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm app python manage.py create_superuser $(cm)

flush:
	docker compose -f local.yml run --rm app python manage.py flush

network-inspect:
	docker network inspect seleccion_docente_local_nw

selecciondocente-db:
	docker compose -f local.yml exec postgres psql --username=postgres --dbname=selecciondocente

django:
	docker-compose -f local.yml exec app $(cmd)