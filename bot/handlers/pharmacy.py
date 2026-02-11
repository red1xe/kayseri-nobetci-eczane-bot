# handlers/pharmacy.py
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import pharmacy_details_keyboard, pharmacy_keyboard, district_keyboard
from services.pharmacy_service import get_pharmacies, get_by_district, get_districts
import re
async def pharmacy_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data

    if data == "back":
        # Go back to pharmacy list
        pharmacies = get_pharmacies()
        current = context.user_data.get("current_district", "all")
        if current == "all":
            pharmacies_filtered = pharmacies
            title = "🏥 *Tüm Nöbetçi Eczaneler*"
        else:
            pharmacies_filtered = get_by_district(pharmacies, current)
            title = f"🏥 *{current} İlçesi Nöbetçi Eczaneler*"

        context.user_data["filtered_pharmacies"] = pharmacies_filtered
        context.user_data["step"] = "pharmacy"

        if not pharmacies_filtered:
            await query.edit_message_text(f"{title}\n\nBu ilçede nöbetçi eczane bulunamadı.", parse_mode="Markdown")
            return

        await query.edit_message_reply_markup(None)
        await query.message.reply_text(
            f"{title}\n\nBir eczane seçin veya konumunuzu göndererek en yakını bulun:",
            reply_markup=pharmacy_keyboard(pharmacies_filtered),
            parse_mode="Markdown"
        )
        return

    if not data.startswith("pharmacy_"):
        return

    pharmacy_id = int(data.split("_", 1)[1])

    pharmacies = context.user_data.get("filtered_pharmacies", [])
    pharmacy = next((p for p in pharmacies if p["id"] == pharmacy_id), None)

    if not pharmacy:
        await query.edit_message_text("Eczane bulunamadı.")
        return
    
    phone_raw = pharmacy.get('phone') or ''
    phone_clean = re.sub(r"[^+\d]", "", str(phone_raw))
    text = (
        f"🏥 *{pharmacy['name']}*\n\n"
        f"📍 Adres: {pharmacy['address']}\n"
        f"📞 Telefon: +9{phone_clean}\n"
        f"🏙 İlçe: {pharmacy['district']}\n"
        f"📍 Semt: {pharmacy['neighborhood']}"
    )

    await query.edit_message_text(
        text,
        reply_markup=pharmacy_details_keyboard(pharmacy),
        parse_mode="Markdown"
    )


async def pharmacy_text_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.strip()

    if text == "⬅ İlçeler":
        pharmacies = context.user_data.get("pharmacies", get_pharmacies())
        districts = get_districts(pharmacies)
        context.user_data["step"] = "district"
        await update.message.reply_text(
            "📍 İlçe seçiniz:",
            reply_markup=district_keyboard(districts)
        )
        return

    pharmacies = context.user_data.get("filtered_pharmacies", [])
    if not pharmacies:
        await update.message.reply_text("Eczane listesi bulunamadı. Lütfen /start ile tekrar başlayın.")
        return

    pharmacy = next((p for p in pharmacies if p["name"] == text), None)
    if not pharmacy:
        await update.message.reply_text("Lütfen listeden geçerli bir eczane seçin.")
        return

    phone_raw = pharmacy.get('phone') or ''
    phone_clean = re.sub(r"[^+\d]", "", str(phone_raw))

    details = (
        f"🏥 *{pharmacy['name']}*\n\n"
        f"- Adres: {pharmacy['address']}\n"
        f"- Telefon: +9{phone_clean}\n"
        f"- İlçe: {pharmacy['district']}\n"
        f"- Semt: {pharmacy['neighborhood']}"
    )

    await update.message.reply_text(
        details,
        reply_markup=pharmacy_details_keyboard(pharmacy),
        parse_mode="Markdown"
    )