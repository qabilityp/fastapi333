FROM python:3.10-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Launch application
FROM python:3.10-slim
WORKDIR /app

# We create a user for security
RUN useradd -m appuser
USER appuser

COPY --from=builder /install /usr/local
COPY . .


EXPOSE 5000

CMD ["python", "main.py"]