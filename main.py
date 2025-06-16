from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"

# Команда /start
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

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📅 Свободные даты":
        await update.message.reply_text("Уточните дату мероприятия (ДД.ММ.ГГГГ), и я проверю доступность.")
    elif text == "📸 Фото":
        await update.message.reply_text("Примеры работ: https://vk.com/your_photos_link")
    elif text == "🎥 Видео":
        await update.message.reply_text("Примеры видео: https://vk.com/wall181769417_4037")
    elif text == "📝 Заполнить анкету":
        await update.message.reply_text("Заполните форму: https://forms.gle/your-form-link")
    else:
        await update.message.reply_text("Пожалуйста, выберите вариант из меню 👇")

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
