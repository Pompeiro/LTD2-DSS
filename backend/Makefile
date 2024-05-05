SOURCE_DIR=dss

build:
	$(DOCKER_COMPOSE) build

run:
	docker compose up -d

lint:
	ruff check app scripts --fix \
    && ruff format app scripts \
    && mypy app
