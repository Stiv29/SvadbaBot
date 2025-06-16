from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"  # ЗАМЕНИ на токен от Svadba73_Bot
ADMIN_ID = 902984899  # Твой Telegram ID

# Шаги анкеты
DATE, LOCATION, GUESTS, BUDGET, WISHES, CONTACTS = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📅 Свободные даты", "📸 Фото"],
        ["🎥 Видео", "📝 Заполнить анкету"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Приветствую!\nЯ — Светлана Мамедова, креативный режиссёр вашей свадьбы!\nПомогаю создать праздник, который запомнится на всю жизнь 💍\n\nВыберите, с чего начнём 👇",
        reply_markup=reply_markup
    )

async def photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Мои фото:\nhttps://vk.com/vedushchaya73")

async def videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 Посмотрите, мои работы:\n"
        "— Видео 1: https://vk.com/wall181769417_4037\n"
        "— Видео 2: https://vkvideo.ru/video-43062629_456239273?t=1m4s"
    )

async def dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Уточните дату мероприятия (ДД.ММ.ГГГГ), и я проверю доступность 😉")

# Анкета - пошаговая форма
async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Ваша дата мероприятия (ДД.ММ.ГГГГ):")
    return DATE

async def form_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("📍 Локация (город, место):")
    return LOCATION

async def form_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("👥 Количество гостей:")
    return GUESTS

async def form_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guests"] = update.message.text
    await update.message.reply_text("💸 Бюджет на ведущего:")
    return BUDGET

async def form_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    await update.message.reply_text("💭 Пожелания по свадьбе:")
    return WISHES

async def form_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wishes"] = update.message.text
    await update.message.reply_text("📲 Контакт (имя и номер/ник):")
    return CONTACTS

async def form_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contacts"] = update.message.text
    summary = "\n".join([f"{k.capitalize()}: {v}" for k, v in context.user_data.items()])
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Новая заявка:\n{summary}")
    await update.message.reply_text("✅ Спасибо! Заявка отправлена, я свяжусь с вами ✨")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Анкета отменена.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("📅 Свободные даты"), dates))
    app.add_handler(MessageHandler(filters.Regex("📸 Фото"), photos))
    app.add_handler(MessageHandler(filters.Regex("🎥 Видео"), videos))

    form_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📝 Заполнить анкету"), form_start)],
        states={
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_date)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_location)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_guests)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_budget)],
            WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_wishes)],
            CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_contacts)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(form_handler)
    app.run_polling()

if __name__ == "__main__":
    main()

