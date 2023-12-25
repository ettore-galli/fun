
PACKAGE=functional

test: 
	@echo "===== TESTING ${PACKAGE} ====="
	pytest tests/

lint:
	@echo "===== LINTING ${PACKAGE} ====="
	black -t py311 ${PACKAGE} tests/
	flake8 ${PACKAGE} tests/
	pylint ${PACKAGE} tests/
	mypy ${PACKAGE} tests/

all: lint test
