install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black app test

lint:
	pylint app &&\
	black app test --check &&\
	bandit -r app -x ./tests

tests:
	pytest

run:
	uvicorn app.main:app --reload
