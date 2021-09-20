.PHONY: help pyenv run format clean check-format lint docs build examples

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

pyenv: ## Install and setup local py env
	python3.9 -m venv venv
	venv/bin/pip install pip-tools
	venv/bin/pip install -r requirements-dev.txt -e .

clean: pyenv ## Clean the project and set everything up
	venv/bin/pip-compile --extra dev -o requirements-dev.txt
	venv/bin/pip-compile -o requirements.txt


run: ## Generate the video and preview
	manim render -ql -p examples/commented.py

lint: ## Run Python linters
	venv/bin/flake8 examples
	venv/bin/flake8 code_video
	venv/bin/pylint examples
	venv/bin/pylint code_video

check-format: lint ## Check Python code formatting
	venv/bin/black examples --check --target-version py38
	venv/bin/black code_video --check --target-version py38
	venv/bin/reorder-python-imports --py38-plus `find code_video -name "*.py"`
	venv/bin/reorder-python-imports --py38-plus `find examples -name "*.py"`

docs: ## Serve the docs
	mkdocs serve -a localhost:8035


format: ## Format Python code
	black code_video --target-version py38
	black examples --target-version py38
	reorder-python-imports --py38-plus `find examples -name "*.py"` || black examples --target-version py38
	reorder-python-imports --py38-plus `find code_video -name "*.py"` || black code_video --target-version py38

build: ## Build docker image
	docker build -t codevidgen-dev --build-arg VERSION=`venv/bin/python setup.py --version` -f docker/Dockerfile .

EXAMPLES_DIR = ./examples
examples: ## Builds all examples
	$(foreach file, $(wildcard $(EXAMPLES_DIR)/*.py), manim render -ql $(file);)

build-examples: pyenv build ## Builds all examples in the docker container
	$(foreach file, $(wildcard $(EXAMPLES_DIR)/*.py), docker run -v $(PWD):/project -w /project --rm codevidgen-dev	manim render -ql $(file);)
