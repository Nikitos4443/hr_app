# Build context is the repo root (uv workspace): docker build -f server/Dockerfile .
FROM ghcr.io/astral-sh/uv:0.13.6 AS uv

FROM dhi.io/python:3.14-dev AS builder
COPY --from=uv /uv /bin/uv
WORKDIR /src
RUN python3 -m venv /venv
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,target=/src \
    uv export --frozen --no-dev --no-editable --package server -o /tmp/requirements.txt && \
    uv pip install --python /venv/bin/python -r /tmp/requirements.txt

FROM dhi.io/python:3.14
WORKDIR /app
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY server/ .

ENV PORT=8000
EXPOSE ${PORT}

CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
