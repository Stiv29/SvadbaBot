from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📅 Свободные даты", "📸 Фото"],
        ["🎥 Видео", "📝 Заполнить анкету"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Я — Светлана Мамедова, креативный режиссёр вашей свадьбы.\n\nВыберите, с чего начнём 👇",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if msg == "📅 Свободные даты":
        await update.message.reply_text("Уточните дату, и я скажу, свободна ли она 🎯")
    elif msg == "📸 Фото":
        await update.message.reply_text("Примеры моих работ: https://vk.com/photo_example")
    elif msg == "🎥 Видео":
        await update.message.reply_text("Видео-примеры: https://vk.com/video_example")
    elif msg == "📝 Заполнить анкету":
        await update.message.reply_text("Заполните анкету: https://forms.gle/example")
    else:
        await update.message.reply_text("Пожалуйста, выбери вариант из меню 👇")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
