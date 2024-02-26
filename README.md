This is the Flight Tracker API. This is compiled using Python 3.11, FastAPI,
pydantic and alembic for data management and database migration.

To start the app - running in Docker is recommended. I've included a Makefile for easy script execution

Once docker containers are up (api and postgresql) go to localhost:8000/docs to start testing out the endpoints.

```bash
$ make up
```
will run the necessary docker compose command

```bash
$ make seed-database
```
will seed the database with the fake data. 

```bash
$ make down
```
will stop the containers whereas;

```bash
$ make down-remove
```
will tear down the containers and images.
