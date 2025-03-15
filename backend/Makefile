SOURCE_DIR=dss

build:
	$(DOCKER_COMPOSE) build

run:
	docker compose up -d

lint:
	uv run ruff check app scripts --fix \
    && uv run ruff format app scripts \
    && uv run mypy app
