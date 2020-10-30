.PHONY: help pyenv run format clean

# Help system from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

pyenv: ## Install and setup local py env
	python3.8 -m venv venv
	venv/bin/pip install -r requirements.txt

clean: pyenv ## Clean the project and set everything up

run: ## Generate the video and preview
	manim main.py CodeSceneDemo  -ql -p

format: ## Format Python code
	black . --target-version py38
