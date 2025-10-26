# telegram-shop (Scaffold)

Kurz: Dieses Repository enthält ein minimal lauffähiges Gerüst für einen Telegram-Bot (Webhook-Modus), PostgreSQL (async SQLAlchemy) und einen BTCPay-Webhook-Endpoint. Das empfohlene Startverfahren für Anfänger ist Docker Compose.

Wichtig: Niemals geheime Werte (z. B. TELEGRAM_TOKEN, BTCPAY_API_KEY) in das öffentliche Repository committen. Nutze `.env` (in `.gitignore`).

Vorbereitung

1. Repository klonen:

   - PowerShell:
     ```powershell
     git clone https://github.com/<DEIN_USER>/<DEIN_REPO>.git
     cd <DEIN_REPO>
     ```

2. Beispiel-Umgebungsdatei anlegen:
   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```
   - Trage mindestens `TELEGRAM_TOKEN` ein.
   - Für Webhook-Tests lokal mit ngrok: lass `TELEGRAM_WEBHOOK_BASE` leer jetzt — siehe Abschnitt "Telegram Webhook (ngrok)".

Start mit Docker (empfohlen)

1. Docker Desktop installieren (Windows) und starten.

2. Projekt mit Docker Compose starten:

   ```powershell
   docker-compose up --build
   ```

   - Service `db` (Postgres) und `app` (Bot) werden gebaut und gestartet.
   - Logs anzeigen: `docker-compose logs -f app`

3. Webhook erreichbar machen (ngrok)
   - Installiere und starte ngrok:
     ```powershell
     ngrok http 8443
     ```
   - Kopiere die angezeigte HTTPS-URL, z. B. `https://abcd1234.ngrok.io`.
   - Öffne `.env`, setze:
     ```
     TELEGRAM_WEBHOOK_BASE=https://abcd1234.ngrok.io
     TELEGRAM_WEBHOOK_PATH=/telegram
     ```
   - App neu starten, damit der Bot den Webhook setzt:
     ```powershell
     docker-compose restart app
     ```
   - Alternativ kannst du den Webhook manuell setzen:
     ```
     https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://abcd1234.ngrok.io/telegram/<TELEGRAM_TOKEN>
     ```

Telegram Webhook — Hinweise

- Telegram verlangt eine gültige HTTPS-URL. ngrok ist praktisch zum lokalen Testen.
- Der Bot setzt den Webhook automatisch beim Start, wenn `TELEGRAM_WEBHOOK_BASE` gesetzt ist. Der Endpoint lautet: `${TELEGRAM_WEBHOOK_BASE}${TELEGRAM_WEBHOOK_PATH}/${TELEGRAM_TOKEN}`

Lokal ohne Docker (nur Entwicklung)

1. Python 3.11 installieren.
2. Virtuelle Umgebung und Abhängigkeiten:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. `.env` anlegen und füllen, dann:
   ```powershell
   python -m bot.bot
   ```

Troubleshooting

- Logs prüfen: `docker-compose logs -f app`
- DB-Verbindungsfehler: prüfe `DATABASE_URL` in `.env` und ob Postgres läuft.
- Bot startet, aber keine Updates: Prüfe Webhook-URL, Firewall/Ports, ngrok-URL.
- `.env` nicht in Git hochladen — `.gitignore` liegt bei.

Was fehlt / nächste Schritte

- Implementierung: Order-Erzeugung, BTCPay-API-Client (Invoice mit metadata.orderId), Verifikation des BTCPay-Webhooks und DB-Updates.
- Optional: Alembic für Migrationen, Tests, CI/CD.

Kurz-Fazit

- Für „einfach kopieren und laufen“: GitHub-Repository klonen, `.env` anlegen, `docker-compose up --build`, ngrok verwenden und `TELEGRAM_WEBHOOK_BASE` setzen. Danach sollte der Bot Webhooks empfangen können.

Wenn gewünscht schreibe ich:

- ein kurzes Script/Entrypoint, das beim Containerstart `create_tables()` sicherstellt (falls noch nötig),
- oder eine GitHub Actions workflow-Datei, die das Image baut und Tests ausführt.
