install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

coverage:
	pytest --cov=src/task_manager --cov-report=html --cov-report=term-missing

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf htmlcov .pytest_cache

lint:
	python -m py_compile $(find src -name "*.py")

all: clean install lint test coverage 