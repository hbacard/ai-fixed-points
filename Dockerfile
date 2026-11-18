# Multi-stage Dockerfile for ai-fixed-points.
#
# Stage 1: install runtime dependencies into an isolated virtual environment
# using the pins from the committed uv.lock (--frozen).
FROM ghcr.io/astral-sh/uv:latest AS builder
WORKDIR /app

# Copy the whole tree (heavy/unwanted files are excluded via .dockerignore)
COPY . .

# Install the locked runtime dependencies plus the package itself into .venv.
# --no-dev keeps the image lean; --no-editable installs a real (copied)
# package rather than an editable link.
RUN uv sync --frozen --no-dev --no-editable

# Stage 2: minimal runtime image, containing only the venv + assets.
FROM python:3.12-slim AS runtime

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 app
USER app
WORKDIR /home/app

ENV PATH="/home/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy the self-contained virtual environment and the runtime assets.
COPY --from=builder /app/.venv /home/app/.venv
COPY --from=builder /app/src /home/app/src
COPY --from=builder /app/prompts /home/app/prompts
COPY --from=builder /app/config.yaml.example /home/app/config.yaml

# Default: welcome message describing how to run the tool.
CMD ["ai-fixed-points", "--help"]
