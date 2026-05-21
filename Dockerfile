FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv pip install --system .
RUN uv pip install --system fastapi uvicorn

EXPOSE 8080

ENV FASTMCP_HOST=0.0.0.0
ENV FASTMCP_PORT=8080

CMD ["uvicorn", "entrypoint:app", "--host", "0.0.0.0", "--port", "8080"]
