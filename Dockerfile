FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

# REPORTMATE_API_URL and REPORTMATE_PASSPHRASE are provided at runtime.
ENTRYPOINT ["reportmate-mcp"]
