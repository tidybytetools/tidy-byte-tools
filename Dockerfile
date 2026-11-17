# Runs the tidy-byte-tools MCP server over stdio (used by Glama's build checks).
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --no-cache-dir . && useradd -m app
USER app
ENTRYPOINT ["tidy-byte-tools-mcp"]
