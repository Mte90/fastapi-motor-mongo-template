# Boilerplate for FastAPI, MongoDB, Motor Projects

Updated for latest version and works :-D

## Features
A new backend project created with this boilerplate provides:
- [x] Asynchronous high-performance RESTful APIs built upon [FastAPI](https://fastapi.tiangolo.com/) framework.
- [x] Asynchronous CRUD operations for a sample resource built upon [Motor](https://motor.readthedocs.io/en/stable/) driver for MongoDB, providing high performance and efficiency.
- [x] API documentation with [Swagger UI](https://swagger.io/tools/swagger-ui/).
- [x] API testing with [pytest](https://docs.pytest.org/en/7.1.x/) and [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio).
- [x] Dockerfile for containerization and docker-compose support.
- [x] Easy package menagement with [Poetry](https://python-poetry.org/).
- [x] Health API for service health checking.
- [x] Easy configuration with environment variables.
- [x] Easy testing, develop running, docker build, docker-compose up and down with Makefile.
- [x] Proper logging with ID masking.

## Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/) installed
- Docker installed
- GNU Make

## Getting Started

```
poetry install --with dev # for dev stuff
poetry install # for production
```

### Edit Environment Variables
Create and edit the `.env` file within the project folder.

### Run Tests
```sh
make test
```

### Build Docker Image
```sh
make docker-build
```

### Docker-compose
```sh
make docker-compose-up
make docker-compose-down
```

### Run Service Locally
```sh
make dev
```

### Check Swagger API Document
Go to ` http://localhost:8888/docs`.
