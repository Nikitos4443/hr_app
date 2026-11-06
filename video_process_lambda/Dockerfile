# Build context is the repo root (uv workspace): docker build -f video_process_lambda/Dockerfile .
FROM ghcr.io/astral-sh/uv:0.13.6 AS uv

FROM public.ecr.aws/lambda/python:3.14
COPY --from=uv /uv /bin/uv
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,target=/src \
    cd /src && \
    uv export --frozen --no-dev --no-emit-workspace --package video-process-lambda -o /tmp/requirements.txt && \
    uv pip install --target "${LAMBDA_TASK_ROOT}" -r /tmp/requirements.txt

# Bake the model into the image so cold starts don't download it from HuggingFace
ARG WHISPER_MODEL=base
ENV WHISPER_MODEL_DIR=/opt/whisper-model
RUN PYTHONPATH="${LAMBDA_TASK_ROOT}" python3 -c \
    "from faster_whisper import download_model; download_model('${WHISPER_MODEL}', output_dir='${WHISPER_MODEL_DIR}')"

COPY video_process_lambda/*.py ${LAMBDA_TASK_ROOT}/

CMD ["app.index"]
