#docker
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

down-remove:
	docker-compose down --rmi all

alembic-make-migrations:
	@echo "creating migration file"
	docker-compose exec api alembic --config flightapi/alembic/alembic.ini revision --autogenerate

seed-database:
	@echo "Seeding database with fake airline data"
	docker-compose exec api python flightapi/db_seed.py