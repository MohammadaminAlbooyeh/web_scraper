FROM python:3.11-slim

WORKDIR /app

# Install build deps (if any) and requirements
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

ENV PYTHONUNBUFFERED=1

# Default command: run the books spider. Override with docker run <image> <cmd>
CMD ["scrapy", "crawl", "books"]
