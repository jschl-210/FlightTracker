FROM python:3.11.4
LABEL maintainers="jis5540@psu.edu"

RUN apt update -y && \
    pip install -U pip && \
    curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1

ENV PATH="/root/.local/bin:$PATH"

ENV FLIGHTAPI_HOME=${FLIGHTAPI_HOME:-/code/flightapi}
ENV FLIGHTAPI_CONFIG=${FLIGHTAPI_CONFIG:-${FLIGHTAPI_HOME}/etc/config.yml}
ENV PYTHONPATH=${FLIGHTAPI_HOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set directory
WORKDIR /code
ENV PYTHONPATH=/code
# install dependencies
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./flightapi /code/flightapi

CMD poetry run python3 -m uvicorn flightapi.main:app --reload --host 0.0.0.0