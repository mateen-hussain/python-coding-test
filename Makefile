install:
		poetry install --no-root

dev:
	  poetry run fastapi dev server.py


test:
	  @echo "Running tests..."
	  poetry run pytest

format:
		@echo "Formatting code..."
		poetry run black .;
		poetry run autoflake .;
		poetry run flake8 . --exclude="src/pdf_service.py" --ignore=E501
		poetry run isort .;

.PHONY: install dev
