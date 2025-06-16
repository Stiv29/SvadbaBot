from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

BOT_TOKEN = "7927069416:AAFEOCMfd3vvtoJeUmbB8nStaSC6dwNSECA"
ADMIN_ID = 902984899  # Твой Telegram ID

# Шаги анкеты
NAME, DATE, LOCATION, GUESTS, PHONE = range(5)

# Старт при входе
async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👰‍♀️ Вас приветствует свадебное агентство Светланы Мамедовой \"MS\".\n"
        "Если Вы здесь, значит до идеальной свадьбы Вас отделяет всего несколько шагов!\n"
        "Заполните анкету и наша команда организует для вас свадьбу мечты!\n\n"
        "Введите Ваше имя:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите дату свадьбы:")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("🏰 Введите локацию проведения:")
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("Сколько гостей планируется?")
    return GUESTS

async def get_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["guests"] = update.message.text
    await update.message.reply_text("Введите Ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    # Получаем юзернейм Telegram аккаунта пользователя
    telegram_username = update.message.from_user.username

    user_data = context.user_data
    summary = (
        f"💌 Новая заявка:\n\n"
        f"👤 Имя: {user_data['name']}\n"
        f"📅 Дата: {user_data['date']}\n"
        f"🏰 Локация: {user_data['location']}\n"
        f"👥 Гостей: {user_data['guests']}\n"
        f"📞 Телефон: {user_data['phone']}\n"
        f"💬 Telegram: @{telegram_username}"  # Добавляем юзернейм Telegram
    )

    # Сообщение админу
    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)

    # Ответ пользователю
    await update.message.reply_text(
        "✨ Благодарим за заявку!\nМы скоро с Вами свяжемся.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анкета отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT | filters.COMMAND, greet_user)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_guests)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()


