.PHONY: setup install dev test lint format clean build run check bumpver help

UV ?= uv

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Create virtual environment and install all dev dependencies
	$(UV) venv
	$(UV) pip install -e ".[dev]"
	$(UV) run pre-commit install

install: ## Install the package in editable mode
	$(UV) pip install -e .

dev: setup ## Full setup: venv + install + pre-commit hooks

test: ## Run the test suite with coverage
	$(UV) run pytest tests/

lint: ## Run linters (ruff)
	$(UV) run ruff check src/ tests/

format: ## Auto-format code (ruff format + isort)
	$(UV) run ruff format src/ tests/
	$(UV) run ruff check --fix src/ tests/

build: ## Build the distribution packages
	$(UV) build

clean: ## Remove build artifacts, caches, and the venv
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage .venv uv.lock
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run: ## Run the CLI directly
	$(UV) run bitssh

check: lint test ## Run lint + test (full CI check)

bumpver-major: ## Bump major version (e.g. 3.7.0 -> 4.0.0)
	$(UV) run bumpver update --major

bumpver-minor: ## Bump minor version (e.g. 3.7.0 -> 3.8.0)
	$(UV) run bumpver update --minor

bumpver-patch: ## Bump patch version (e.g. 3.7.0 -> 3.7.1)
	$(UV) run bumpver update --patch