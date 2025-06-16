from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"  # ← твой токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Приветствую!\n"
        "Я — Светлана Мамедова, креативный режиссёр вашей свадьбы!\n\n"
        "Выберите, с чего начнём:\n"
        "📅 Свободные даты\n📸 Фото\n🎥 Видео\n📝 Заполнить анкету"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()
