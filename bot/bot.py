# filepath: telegram-shop/telegram-shop/bot/bot.py
import os
import asyncio
import logging
from typing import Optional

from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# handlers
from bot.handlers.commands import start, buy

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# ---------------------------
# Konfiguration / Environment
# ---------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Telegram Bot Token
TELEGRAM_WEBHOOK_BASE = os.getenv("TELEGRAM_WEBHOOK_BASE")  # z.B. https://example.com
TELEGRAM_WEBHOOK_PATH = os.getenv("TELEGRAM_WEBHOOK_PATH", "/telegram")
TELEGRAM_LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
TELEGRAM_LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8443"))

# DB settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/telegram_shop"
)

# ---------------------------
# Datenbank (SQLAlchemy Async)
# ---------------------------
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(128), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    status = Column(String(32), default="created")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Datenbank-Tabellen geprüft/erstellt.")

# ---------------------------
# HTTP Handlers (aiohttp)
# ---------------------------
async def telegram_webhook(request: web.Request) -> web.Response:
    app: Application = request.app["ptb_app"]
    try:
        data = await request.json()
    except Exception as e:
        logger.exception("Fehler beim Lesen des Telegram-Request JSON: %s", e)
        return web.Response(status=400, text="invalid json")

    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return web.Response(text="OK")

async def btcpay_webhook(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        payload = await request.text()
    logger.info("Eingehender BTCPay-Webhook: %s", payload)
    # TODO: Validierung (HMAC/shared secret), extrahiere metadata.orderId, update DB, notify user
    return web.Response(text="OK")

# ---------------------------
# Main: Application starten
# ---------------------------
async def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN fehlt. Bitte setzen Sie die Umgebungsvariable.")
        return

    await create_tables()

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("buy", buy))

    await application.initialize()
    await application.start()
    logger.info("telegram-application gestartet.")

    if TELEGRAM_WEBHOOK_BASE:
        webhook_url = TELEGRAM_WEBHOOK_BASE.rstrip("/") + TELEGRAM_WEBHOOK_PATH.rstrip("/") + f"/{TELEGRAM_TOKEN}"
        await application.bot.set_webhook(webhook_url)
        logger.info("Telegram webhook gesetzt: %s", webhook_url)
    else:
        logger.warning("TELEGRAM_WEBHOOK_BASE nicht gesetzt. Bitte set webhook manuell, wenn nötig.")

    aio_app = web.Application()
    aio_app["ptb_app"] = application
    aio_app.router.add_post(f"{TELEGRAM_WEBHOOK_PATH.rstrip('/')}/{TELEGRAM_TOKEN}", telegram_webhook)
    aio_app.router.add_post("/btcpay-webhook", btcpay_webhook)

    runner = web.AppRunner(aio_app)
    await runner.setup()
    site = web.TCPSite(runner, TELEGRAM_LISTEN_HOST, TELEGRAM_LISTEN_PORT)
    await site.start()
    logger.info("HTTP Server gestartet auf %s:%d", TELEGRAM_LISTEN_HOST, TELEGRAM_LISTEN_PORT)

    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutdown initiiert.")
    finally:
        await runner.cleanup()
        await application.stop()
        await application.shutdown()
        await engine.dispose()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())