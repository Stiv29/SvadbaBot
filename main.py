import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

# Вставь сюда свой токен
BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"
ADMIN_ID = 902984899  # ID админа (твой Telegram ID)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Состояния для анкеты
DATE, LOCATION, GUESTS, BUDGET, WISHES, CONTACT = range(6)

# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📅 Свободные даты", "📸 Фото"],
        ["🎥 Видео", "📝 Заполнить анкету"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Приветствую!\nЯ — Светлана Мамедова, креативный режиссёр вашей свадьбы!\n"
        "Выберите, с чего начнём 👇",
        reply_markup=reply_markup
    )

# Ответы на кнопки
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📅 Свободные даты":
        await update.message.reply_text("📆 Напишите дату вашего мероприятия (ДД.ММ.ГГГГ):")
    elif text == "📸 Фото":
        await update.message.reply_text("📸 Примеры работ: https://vk.com/vedushchaya73")
    elif text == "🎥 Видео":
        await update.message.reply_text(
            "🎥 Смотрите, как я веду свадьбы:\n"
            "Видео 1: https://vk.com/wall181769417_4037\n"
            "Видео 2: https://vkvideo.ru/video-43062629_456239273?t=1m4s"
        )
    elif text == "📝 Заполнить анкету":
        await update.message.reply_text("📅 Ваша дата мероприятия (ДД.ММ.ГГГГ):")
        return DATE

# Анкета
async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("📍 Укажите город и локацию:")
    return LOCATION

async def ask_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("👥 Сколько гостей ожидается?")
    return GUESTS

async def ask_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guests"] = update.message.text
    await update.message.reply_text("💸 Какой ориентировочный бюджет?")
    return BUDGET

async def ask_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    await update.message.reply_text("💭 Ваши пожелания?")
    return WISHES

async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wishes"] = update.message.text
    await update.message.reply_text("📲 Ваше имя и телефон или Telegram:")
    return CONTACT

async def finish_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    data = context.user_data
    message = (
        "📥 Новая заявка!\n\n"
        f"Дата: {data['date']}\n"
        f"Локация: {data['location']}\n"
        f"Гости: {data['guests']}\n"
        f"Бюджет: {data['budget']}\n"
        f"Пожелания: {data['wishes']}\n"
        f"Контакты: {data['contact']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text("✅ Спасибо! Ваша заявка отправлена.")
    return ConversationHandler.END

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Анкета отменена.")
    return ConversationHandler.END

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    form_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📝 Заполнить анкету"), handle_text)],
        states={
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_guests)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_budget)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_wishes)],
            WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_form)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(form_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()


