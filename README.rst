

Config variables -- other than those passed in by environment are in the config.py file.

To run the app in local development with reload
`GRAPHQL_KEY=hasura_graphql_api_key BASIC_USERNAME=books BASIC_PASSWORD=default uvicorn app.main:app --reload`

In Windows, this works too:
set GRAPHQL_KEY=***********
set BASIC_USERNAME=books
set BASIC_PASSWORD=************

uvicorn app.main:app --reload`
