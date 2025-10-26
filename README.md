# telegram-shop (Scaffold)

Kurz: Minimaler Telegram-Bot (Webhook-Modus) + PostgreSQL + BTCPay-Webhook-Endpoint. Ziel: Jeder soll das Repo klonen und mit Docker + ngrok schnell laufen haben.

Wichtig: Niemals Secrets (z. B. TELEGRAM_TOKEN, BTCPAY_API_KEY) in ein öffentliches Repo committen. Nutze `.env` (ist in `.gitignore`).

## Voraussetzungen

- Docker Desktop (Windows) installiert und gestartet
- Git installiert
- Optional: ngrok (https://ngrok.com) zum lokalen Testen von Webhooks

## Schnellstart (empfohlen: Docker)

Im Projekt-Root (z. B. `c:\projects\telegram-shop\telegram-shop`):

1. Repo klonen

```powershell
git clone https://github.com/<DEIN_USER>/<DEIN_REPO>.git
cd <DEIN_REPO>
```

2. Beispiel-Env kopieren und bearbeiten

```powershell
Copy-Item .env.example .env
notepad .env
```

Mindestwerte setzen: `TELEGRAM_TOKEN`. Für lokalen Webhook-Test zunächst `TELEGRAM_WEBHOOK_BASE` leer lassen.

3. Docker-Container bauen und starten

```powershell
docker-compose up --build -d
```

- Startet `db` (Postgres) und `app` (Bot).
- Logs ansehen: `docker-compose logs -f app`

4. (Lokal testen) ngrok starten und Webhook konfigurieren

- Starte ngrok:

```powershell
ngrok http 8443
```

- Kopiere die HTTPS-URL (z. B. `https://abcd1234.ngrok.io`) und setze in `.env`:

```
TELEGRAM_WEBHOOK_BASE=https://abcd1234.ngrok.io
TELEGRAM_WEBHOOK_PATH=/telegram
```

- App neu starten, damit der Bot den Webhook setzt:

```powershell
docker-compose restart app
```

- Alternativ manuell setzen:

```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://abcd1234.ngrok.io/telegram/<TELEGRAM_TOKEN>
```

5. Testen im Telegram:

- Öffne deinen Bot in Telegram und sende `/start` oder `/buy`.

## Lokal ohne Docker (Entwicklung)

1. Python 3.11 installieren
2. Virtuelle Umgebung & Abhängigkeiten:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. `.env` anlegen und füllen, dann:

```powershell
python -m bot.bot
```

## Wichtige Hinweise / Troubleshooting

- Telegram-Webhooks benötigen HTTPS. Verwende ngrok oder eine echte Domain mit TLS.
- Prüfe Logs: `docker-compose logs -f app`
- DB-Fehler: `DATABASE_URL` prüfen und ob Postgres-Container läuft (`docker-compose ps`).
- `.env` nie committen.

## Sicherheit & Produktion

- Verwende echte Domain + TLS (Let's Encrypt) für Produktion.
- Schütze BTCPay-Webhook-Endpoint (Signatur/HMAC) — noch zu implementieren.
- Secrets in CI/CD bzw. Secret-Manager speichern, nicht im Repo.

## Nächste Schritte (empfohlen)

- Order-Erzeugung und Invoice-Erstellung (BTCPay) implementieren (metadata.orderId).
- BTCPay-Webhook-Verifikation (HMAC/shared secret) implementieren.
- Alembic für DB-Migrationen hinzufügen, Tests und CI.

Wenn du willst, erstelle ich als nächstes:

- ein kleines Entrypoint-Script, das beim Containerstart `create_tables()` ausführt, oder
- Scaffolding für BTCPay-Invoice + Webhook-Verifikation.
