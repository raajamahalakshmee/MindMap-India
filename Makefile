# Makefile for Mindmap India
# Provides shortcuts for common development tasks

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
MYPY = mypy
STREAMLIT = streamlit

# Default target (run when you just type 'make')
.DEFAULT_GOAL := help

# Help target to show all available commands
help:
	@echo "Mindmap India - Development Commands"
	@echo ""
	@echo "  install           Install all dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  run              Run the Streamlit app"
	@echo "  test             Run tests"
	@echo "  test-cov         Run tests with coverage report"
	@echo "  lint             Run all linters"
	@echo "  format           Format code with Black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo "  docs             Build documentation"
	@echo "  clean            Clean up build artifacts"
	@echo "  help             Show this help message"

# Install all dependencies
install:
	$(PIP) install -r requirements.txt

# Install development dependencies
install-dev:
	$(PIP) install -r requirements-dev.txt
	pre-commit install

# Run the Streamlit app
run:
	$(STREAMLIT) run app/app.py

# Run tests
test:
	$(PYTEST) tests/

# Run tests with coverage
test-cov:
	$(PYTEST) --cov=app --cov-report=term-missing --cov-report=html tests/

# Run all linters
lint:
	@echo "Running Black..."
	$(BLACK) --check .
	@echo "\nRunning isort..."
	$(ISORT) --check-only .
	@echo "\nRunning flake8..."
	$(FLAKE8) .
	@echo "\nRunning mypy..."
	$(MYPY) .

# Format code
format:
	$(BLACK) .
	$(ISORT) .

# Run type checking
type-check:
	$(MYPY) .

# Build documentation
docs:
	@echo "Building documentation..."
	cd docs && make html
	@echo "\nDocumentation built. Open docs/_build/html/index.html in your browser."

# Clean up build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete
	find . -type f -name "*~" -delete
	find . -type f -name "*.bak" -delete
	find . -type f -name "*.swp" -delete
	find . -type f -name ".coverage" -delete

# Phony targets (don't represent files)
.PHONY: help install install-dev run test test-cov lint format type-check docs clean
