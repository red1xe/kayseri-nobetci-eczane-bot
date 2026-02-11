# handlers/location.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from services.distance_service import find_nearest
from services.pharmacy_service import add_distances
from keyboards.inline import pharmacy_details_keyboard

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_location = update.message.location
    pharmacies = context.user_data.get("filtered_pharmacies", context.user_data.get("pharmacies", []))

    # If user previously requested directions to a specific pharmacy, build Google Maps directions
    dest = context.user_data.pop("directions_destination", None)
    if dest:
        origin_lat = user_location.latitude
        origin_lon = user_location.longitude
        dest_lat = dest.get("lat")
        dest_lon = dest.get("lon")

        url = f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lon}&destination={dest_lat},{dest_lon}&travelmode=driving"

    
        # remove the request-location keyboard and send the directions link
        await update.message.reply_text(f"Yol tarifi hazır:\n\n{url}", reply_markup=ReplyKeyboardRemove())
        return

    if not pharmacies:
        await update.message.reply_text("Eczane listesi bulunamadı. Lütfen /start ile tekrar başlayın.")
        return

    # Add distances to pharmacies based on user location
    pharmacies_with_distances = add_distances(pharmacies, user_location.latitude, user_location.longitude)

    # Sort pharmacies by distance
    nearest = sorted(pharmacies_with_distances, key=lambda p: float(p["distanceKm"].split()[0]))[0]

    text = (
        f"📍 *En Yakın Eczane*\n\n"
        f"🏥 {nearest['name']}\n"
        f"📍 Adres: {nearest['address']}\n"
        f"🏙 İlçe: {nearest['district']}\n"
        f"📍 Semt: {nearest['neighborhood']}\n"
        f"📏 Uzaklık: {nearest['distanceKm']}"
    )

    await update.message.reply_text(
        text,
        reply_markup=pharmacy_details_keyboard(nearest),
        parse_mode="Markdown"
    )
