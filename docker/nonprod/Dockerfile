FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG USER

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /sih_project

RUN useradd -ms /bin/bash $USER && \
    usermod -aG root $USER && \
    chown -R $USER:$USER /sih_project && \
    chmod -R 755 /sih_project

RUN chmod -R g+w /usr/local/

USER $USER

# Ensure the installed binary is on the `PATH`
ENV PATH="/home/$USER/.local/bin/:$PATH"

COPY pyproject.toml .
COPY uv.lock .
RUN uv lock
RUN uv sync --locked
