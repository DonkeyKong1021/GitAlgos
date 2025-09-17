.PHONY: install fmt lint typecheck test up down migrate seed clean coverage

install:
	pip install -e .

fmt:
	black app tests
	ruff format app tests

lint:
	ruff check app tests

typecheck:
	mypy app

coverage:
	pytest --cov=app --cov-report=term-missing

test:
	pytest

up:
	docker-compose up --build

down:
	docker-compose down

migrate:
	alembic upgrade head

seed:
	python -m app.workers.tasks seed_strategies

clean:
	rm -rf .pytest_cache .mypy_cache
