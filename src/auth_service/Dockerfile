FROM python:3.12-slim AS builder
WORKDIR /app
COPY src/auth_service/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --no-create-home appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY src/auth_service/main.py .
COPY src/auth_service/models.py .
COPY src/auth_service/security.py .
COPY src/auth_service/database.py .
COPY src/auth_service/private.pem .
COPY src/auth_service/public.pem .

# Bulletproof Security Patch for local environments
RUN chown appuser:appuser /app /app/* && \
    chmod 644 private.pem public.pem main.py security.py models.py database.py

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
