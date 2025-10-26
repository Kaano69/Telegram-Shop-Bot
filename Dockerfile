FROM python:3.11-slim

WORKDIR /app

# System deps for asyncpg / sql drivers
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere Projekt
COPY . .

ENV PYTHONUNBUFFERED=1

# Start the bot as a module so relative package imports funktionieren
CMD ["python", "-m", "bot.bot"]