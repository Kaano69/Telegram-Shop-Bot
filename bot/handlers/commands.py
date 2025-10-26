from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo! Bot läuft. Nutze /buy um ein Produkt zu kaufen (Platzhalter).")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Platzhalter: später Order erzeugen, DB-Eintrag, BTCPay-Invoice anfordern
    await update.message.reply_text("Hier würde eine Order erstellt und eine BTCPay-Invoice erzeugt. (Noch nicht implementiert)")