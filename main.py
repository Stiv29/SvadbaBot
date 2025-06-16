from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

# 🔐 Твой токен
BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"

# 👤 Telegram ID администратора
ADMIN_ID = 902984899

# Состояния анкеты
DATE, LOCATION, GUESTS, BUDGET, WISHES, CONTACTS = range(6)

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [["📅 Свободные даты", "📸 Фото"], ["🎥 Видео", "📝 Заполнить анкету"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Приветствую!\n"
        "Я — Светлана Мамедова, креативный режиссёр вашей свадьбы! 💍\n"
        "Выберите, с чего начнём 👇",
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📅 Свободные даты":
        await update.message.reply_text("📆 Уточните дату свадьбы (ДД.ММ.ГГГГ):")
    elif text == "📸 Фото":
        await update.message.reply_text("Примеры фото работ: https://vk.com/vedushchaya73")
    elif text == "🎥 Видео":
        await update.message.reply_text(
            "Видео 1: https://vk.com/wall181769417_4037\n"
            "Видео 2: https://vkvideo.ru/video-43062629_456239273?t=1m4s"
        )
    elif text == "📝 Заполнить анкету":
        await update.message.reply_text("📅 Ваша дата мероприятия (ДД.ММ.ГГГГ):")
        return DATE

# 📝 Анкета шаги
async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("📍 Укажите локацию:")
    return LOCATION

async def ask_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("👥 Сколько гостей?")
    return GUESTS

async def ask_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guests"] = update.message.text
    await update.message.reply_text("💸 Ориентировочный бюджет на ведущего?")
    return BUDGET

async def ask_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    await update.message.reply_text("💭 Расскажите о ваших пожеланиях:")
    return WISHES

async def ask_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wishes"] = update.message.text
    await update.message.reply_text("📲 Ваше имя и телефон/Telegram:")
    return CONTACTS

async def submit_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contacts"] = update.message.text
    data = context.user_data
    text = (
        f"📩 Новая заявка:\n\n"
        f"Дата: {data['date']}\n"
        f"Локация: {data['location']}\n"
        f"Гости: {data['guests']}\n"
        f"Бюджет: {data['budget']}\n"
        f"Пожелания: {data['wishes']}\n"
        f"Контакты: {data['contacts']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await update.message.reply_text("✅ Спасибо! Ваша заявка отправлена.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Анкета отменена.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    form = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📝 Заполнить анкету$"), handle_message)],
        states={
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_guests)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_budget)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_wishes)],
            WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contacts)],
            CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, submit_form)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(form)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()


