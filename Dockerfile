FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir ".[http]"

# Expose stdio MCP transport (default)
ENTRYPOINT ["click-to-mcp"]
CMD ["--help"]
