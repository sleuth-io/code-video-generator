.PHONY: help pyenv run format clean check-format lint docs build examples

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

pyenv: ## Install and setup local py env
	python3.8 -m venv venv
	venv/bin/pip install -r requirements.txt
	cd venv/lib/python3.8/site-packages && git apply ../../../../patches/639.diff && cd -

clean: pyenv ## Clean the project and set everything up

run: ## Generate the video and preview
	manim examples/commented.py -ql -p

lint: ## Run Python linters
	flake8 examples
	flake8 code_video
	pylint examples
	pylint code_video

check-format: lint ## Check Python code formatting
	black examples --check --target-version py38
	black code_video --check --target-version py38
	reorder-python-imports --py38-plus `find code_video -name "*.py"`
	reorder-python-imports --py38-plus `find examples -name "*.py"`

docs: ## Serve the docs
	mkdocs serve -a localhost:8035


format: ## Format Python code
	black code_video --target-version py38
	black examples --target-version py38
	reorder-python-imports --py38-plus `find examples -name "*.py"` || black examples --target-version py38
	reorder-python-imports --py38-plus `find code_video -name "*.py"` || black code_video --target-version py38

build: ## Build docker image
	docker build -t codevidgen-dev --build-arg VERSION=`python setup.py --version` -f docker/Dockerfile .

EXAMPLES_DIR = ./examples
examples: ## Builds all examples
	$(foreach file, $(wildcard $(EXAMPLES_DIR)/*.py), manim -ql $(file);)

build-examples: build ## Builds all examples in the docker container
	$(foreach file, $(wildcard $(EXAMPLES_DIR)/*.py), docker run -v $(PWD):/project -w /project --rm codevidgen-dev	manim -ql $(file);)
