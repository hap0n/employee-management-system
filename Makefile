.PHONY: verify_env fmt dev test build build_dev build_test

verify_env:
	python scripts/dotenv_diff.py -r

fmt:
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports .
	isort -rc src tests
	black . -l 120

dev: verify_env fmt
	docker-compose up --abort-on-container-exit

test: fmt
	python setup.py flake8
	docker-compose -f docker-compose-test.yml up --abort-on-container-exit

build: build_dev

build_dev:
	docker-compose build --parallel

build_test:
	docker-compose -f docker-compose-test.yml build --parallel
