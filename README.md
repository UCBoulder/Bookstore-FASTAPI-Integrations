# Bookstore REST API

Provides RESTful API interface(s) for UCB Bookstore data.

Config variables -- other than those passed in by environment are in the config.py file.

## Local Development

### Environment Vars

Set environment variables for GRAPHQL_KEY, BASIC_USERNAME, and BASIC_PASSWORD. For ex:

```shell
#bash
export KEYNAME="123"

#windows cmd
set KEYNAME=123

#windows powershell
$Env:KEYNAME="123"
```

### Format, Lint, Test, and Run

1. To format your code, run `make format`
1. To lint your code, run `make lint`
1. To test your code, run `make tests`
1. To run uvicorn locally, run `make uvicorn-run`

## Container'ing

### Build

```shell
make docker-build
```

### Run

```shell
make docker-run
``` 