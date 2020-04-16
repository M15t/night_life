SHELL=./scripts/make-venv.sh #must update each project
.DEFAULT_GOAL := help


# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


depends: ## Provision dev environment
	pip install -r ./requirements.txt
	docker-compose up -d
	@$(MAKE) migrate

start: ## Bring up the server on dev environment
	docker-compose up -d
	scripts/waitdb.sh
	python manage.py runserver 0.0.0.0:8080

migrate: ## Run database migrations
	python manage.py makemigrations
	python manage.py migrate

deploy: ## Alias of stg.deploy
	stg.deploy 

stg.deploy: ## Deploy to customer STG server
	scripts/deployer.sh stg

prod.deploy: ## Deploy to customer PROD server
	scripts/deployer.sh prod
