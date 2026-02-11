# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from services.pharmacy_service import get_pharmacies, get_districts
from keyboards.inline import district_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pharmacies = get_pharmacies()
    context.user_data["pharmacies"] = pharmacies
    context.user_data["step"] = "district"

    districts = get_districts(pharmacies)
    await update.message.reply_text(
        "📍 İlçe seçiniz:",
        reply_markup=district_keyboard(districts)
    )
