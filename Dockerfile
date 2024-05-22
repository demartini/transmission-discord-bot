# Use the official Python image as base
FROM python:3-slim-bullseye as python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR $PYSETUP_PATH

# Copy the poetry files
COPY ./poetry.lock ./pyproject.toml ./

# Install project dependencies
RUN poetry install --no-root --no-dev

FROM python-base as runtime

# Copy the source code into the container
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY src/ /app
WORKDIR /app

# Run the bot
CMD ["python", "-u", "main.py"]
