FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]