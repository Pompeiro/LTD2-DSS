DOCKER_COMPOSE=docker compose -f docker-compose.yml
SOURCE_DIR=dss

build:
	$(DOCKER_COMPOSE) build

run:
	$(DOCKER_COMPOSE) up

lint:
	$(DOCKER_COMPOSE) run --rm backend /bin/sh -c "\
		isort $(SOURCE_DIR) \
		&& black $(SOURCE_DIR) \
		&& mypy $(SOURCE_DIR) \
		&& pylint -j 4 $(SOURCE_DIR)"

test:
	$(DOCKER_COMPOSE) run --rm backend pytest $(SOURCE_DIR)/tests