# keyboards/inline.py
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

def district_keyboard(districts):
    keyboard = [
        [KeyboardButton(d)]
        for d in districts
    ]
    keyboard.append([KeyboardButton("Tüm İlçeler")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def pharmacy_keyboard(pharmacies):
    keyboard = [
        [KeyboardButton(p["name"])]
        for p in pharmacies
    ]
    keyboard.append([KeyboardButton("⬅ İlçeler")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def pharmacy_details_keyboard(pharmacy):

    keyboard = []
    
    keyboard.append([InlineKeyboardButton("🗺 Harita", url=f"https://www.google.com/maps?q={pharmacy['latitude']},{pharmacy['longitude']}")])
    keyboard.append([InlineKeyboardButton("🧭 Yol tarifi al", callback_data=f"directions_{pharmacy['latitude']}_{pharmacy['longitude']}")])
    keyboard.append([InlineKeyboardButton("⬅ Geri", callback_data="back")])
    
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update, context):
    query = update.callback_query
    # answer the callback with contextual messages per-action below
    if query.data.startswith("directions_"):   
        # parse destination coordinates from callback data and request user's location
        try:
            coords = query.data.replace("directions_", "").split("_")
            dest_lat = float(coords[0])
            dest_lon = float(coords[1])
        except Exception:
            await query.answer(text="Yol tarifi için hedef koordinatlar alınamadı.", show_alert=True)
            await query.edit_message_text("Yol tarifi için hedef koordinatlar alınamadı.")
            return

        # store destination in user_data and ask user to share their location
        context.user_data["directions_destination"] = {"lat": dest_lat, "lon": dest_lon}

        kb = ReplyKeyboardMarkup(
            [[KeyboardButton("Konumumu Gönder", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        # let the user know we asked for their location
        await query.answer(text="Konum paylaşımı için hazır. Lütfen konumunuzu gönderin.")
        await query.message.reply_text("Lütfen konumunuzu paylaşın; size yol tarifi göndereceğim.", reply_markup=kb)
        return

    # fallback: ensure callback is answered if no branch matched
    await query.answer()