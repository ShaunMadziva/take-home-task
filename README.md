# Technical Test Template

## Submission by: Shaun Madziva

I've used the template as provided and added my code in `user_monitoring/api.py` and my unit tests in `tests/api_test.py`.  
I managed to attempt all the conditions and left comments in the code to explain my thinking.


## Getting started

We have set up a basic Flask API that runs on port `5000` and included a `pytest` test showing the endpoint working.

If you prefer to use FastAPI, Django or other Python packages, feel free to add any you want using Poetry.
We have included a `Makefile` for conveince but you are free to run the project however you want.

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{ }'
```