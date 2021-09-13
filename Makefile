.PHONY: dev build build_dev fmt verify_env

fmt:
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports .
	isort -rc src
	black . -l 120

verify_env:
	python scripts/dotenv_diff.py -r

dev: verify_env fmt
	docker-compose up --abort-on-container-exit

build: build_dev

build_dev:
	docker-compose build --parallel


