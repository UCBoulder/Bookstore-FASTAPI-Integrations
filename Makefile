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

uvicorn-run:
	uvicorn app.main:app --reload
	
docker-build:
	docker build -t bookstore-api .

docker-run:
	docker run -d --name bookstore-api \
	-p 8988:80 \
	-e GRAPHQL_KEY=${GRAPHQL_KEY} \
	-e BASIC_USERNAME=${BASIC_USERNAME} \
	-e BASIC_PASSWORD=${BASIC_PASSWORD} \
	bookstore-api
