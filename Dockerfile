FROM python:3-slim-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

FROM python-base AS builder-base

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /opt/pysetup
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --without=dev

COPY ./src /opt/pysetup/src

FROM python-base AS runtime
COPY --from=builder-base /opt/pysetup /opt/pysetup
COPY ./src /app
WORKDIR /app
CMD ["python", "-u", "main.py"]
