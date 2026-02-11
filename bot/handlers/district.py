# handlers/district.py
from telegram import Update
from telegram.ext import ContextTypes
from services.pharmacy_service import get_pharmacies, get_by_district, get_districts
from keyboards.inline import district_keyboard, pharmacy_keyboard

async def district_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    selected = None
    if query:
        await query.answer()
        selected = query.data
    elif update.message:
        selected = update.message.text.strip()

    if not selected:
        if update.message:
            await update.message.reply_text("Bir hata oluştu. Lütfen tekrar deneyin.")
        return

    pharmacies = get_pharmacies()
    districts = get_districts(pharmacies)

    if selected in ("all", "Tüm İlçeler"):
        pharmacies_filtered = pharmacies
        title = "🏥 *Tüm Nöbetçi Eczaneler*"
        context.user_data["current_district"] = "all"
    elif selected == "back":
        current = context.user_data.get("current_district", "all")
        if current == "all":
            pharmacies_filtered = pharmacies
            title = "🏥 *Tüm Nöbetçi Eczaneler*"
        else:
            pharmacies_filtered = get_by_district(pharmacies, current)
            title = f"🏥 *{current} İlçesi Nöbetçi Eczaneler*"
    else:
        if selected not in districts:
            if update.message:
                await update.message.reply_text(
                    "Lütfen listeden geçerli bir ilçe seçin.",
                    reply_markup=district_keyboard(districts)
                )
            return
        pharmacies_filtered = get_by_district(pharmacies, selected)
        title = f"🏥 *{selected} İlçesi Nöbetçi Eczaneler*"
        context.user_data["current_district"] = selected

    context.user_data["filtered_pharmacies"] = pharmacies_filtered
    context.user_data["step"] = "pharmacy"

    if not pharmacies_filtered:
        message = query.message if query else update.message
        await message.reply_text(
            f"{title}\n\nBu ilçede nöbetçi eczane bulunamadı.",
            parse_mode="Markdown"
        )
        return

    message = query.message if query else update.message
    await message.reply_text(
        f"{title}\n\nBir eczane seçin veya konumunuzu göndererek en yakını bulun:",
        reply_markup=pharmacy_keyboard(pharmacies_filtered),
        parse_mode="Markdown"
    )
