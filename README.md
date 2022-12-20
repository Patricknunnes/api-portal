
# API Portal IDOR

## Summary
- [1. Goals](#goals)
- [2. Technologies and tools](#technologies-and-tools)
- [3. Running the application](#running-the-application)
- [4. More docs](#more-docs)

## Goals
This API will be used to grant access to Portal IDOR website, as well as to manage users data through database interaction.

## Technologies and tools
| Technology | Goal |
|-----------|------|
| Docker/Docker-compose | Containerizing application |
| Pylama | Code audit tool for Python |
| Alembic  | Database migration tool |
| FastAPI  | Web framework for building APIs with Python |

## Running the application

Once the repository is cloned, change the current branch to `develop`

    git checkout develop

Create and activate a virtual environment

    python3 -m venv venv && source venv/bin/activate

Install dependencies

    python3 -m pip install -r requirements.txt

Copy `.env_example` to `.env`

    cp .env_example .env

Fill the variables according to the values in the end of document ***IDOR: Termo de abertura do projeto***

For running both API and database with docker

    docker-compose up -d

> In order to run only database with docker, run  `docker-compose up -d postgres`
> If you wish to run only the API with docker, run  `docker-compose up -d api`

Running both API and database with docker,  will automatically run alembic migrations. Otherwise, you can run them with

    make db_create

In order to run the API without docker, run

    make dev_server

After that, you can access the API's docs through `http://localhost:8080/docs`

## More docs
- [Creating OpenID Connect Authentication Provider](./docs/sso/Creating%20OpenID%20Connect%20Auth%20Provider.md)

- [Registering OpenID Connect Authentication Provider on Canvas](./docs/canvas/Registering%20OpenId%20Connect%20Auth%20Provider.md)

