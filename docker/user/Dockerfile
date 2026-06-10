FROM python:3.12-slim AS builder
WORKDIR /app
COPY src/user_service/requirements.txt .
RUN pip install --upgrade pip && pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

RUN adduser --disabled-password --no-create-home --uid 1001 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY src/user_service/main.py .
COPY src/user_service/models.py .
COPY src/user_service/dependencies.py .
COPY src/auth_service/public.pem .

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
