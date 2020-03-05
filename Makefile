build:
	poetry build

install:
	poetry install

publish:
	poetry publish -r testpypi

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest gendiff tests