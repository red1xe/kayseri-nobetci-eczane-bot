from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from handlers.start import start
from handlers.district import district_selected
from handlers.location import location_handler
from handlers.pharmacy import pharmacy_selected, pharmacy_text_selected
from keyboards.inline import button_handler

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def text_router(update, context):
    step = context.user_data.get("step")
    if step == "pharmacy":
        return await pharmacy_text_selected(update, context)
    return await district_selected(update, context)


app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler, pattern=r"^directions_"))
app.add_handler(CallbackQueryHandler(pharmacy_selected, pattern=r"^(pharmacy_|back$)"))
app.add_handler(MessageHandler(filters.LOCATION, location_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
app.run_polling()
