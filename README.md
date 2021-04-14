# Bookstore REST API

Config variables -- other than those passed in by environment are in the config.py file.

To run the app in local development with reload,
```
GRAPHQL_KEY=hasura_graphql_api_key BASIC_USERNAME=books BASIC_PASSWORD=default uvicorn app.main:app --reload
```

In Windows, this works too:
```
set GRAPHQL_KEY=*********** set BASIC_USERNAME=books set BASIC_PASSWORD=password  uvicorn app.main:app --reload
```

## Container'ing

``` 
docker build -t bookstore-api . 
docker run -d --name bookstore-api \ 
-p 8988:80 \ 
-e GRAPHQL_KEY=**** \ 
-e BASIC_USERNAME=books \ 
-e BASIC_PASSWORD=password \ 
bookstore-api
```
