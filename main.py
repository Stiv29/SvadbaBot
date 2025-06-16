
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "7927069416:AAE3Irs2UoW1cxvLZsVGXuRG8xynN78KKxs"
ADMIN_ID = 902984899  # ← твой Telegram ID

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["📅 Свободные даты", "📸 Фото"],
        ["🎥 Видео", "📝 Заполнить анкету"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Приветствую!\nЯ — Светлана Мамедова, креативный режиссёр вашей свадьбы!\nВыберите, с чего начнём 👇",
        reply_markup=menu_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📅 Свободные даты":
        await update.message.reply_text("Уточните, пожалуйста, дату (ДД.ММ.ГГГГ), я проверю доступность 🎯")
    elif text == "📸 Фото":
        await update.message.reply_text("Фото: https://vk.com/album-43062629_265386130")
    elif text == "🎥 Видео":
        await update.message.reply_text("Видео: https://vk.com/wall181769417_4037")
    elif text == "📝 Заполнить анкету":
        await update.message.reply_text("📅 Напишите дату свадьбы:")
        context.user_data["step"] = "date"
    elif "step" in context.user_data:
        step = context.user_data["step"]
        if step == "date":
            context.user_data["date"] = text
            await update.message.reply_text("📍 Укажите локацию:")
            context.user_data["step"] = "location"
        elif step == "location":
            context.user_data["location"] = text
            await update.message.reply_text("👥 Сколько гостей?")
            context.user_data["step"] = "guests"
        elif step == "guests":
            context.user_data["guests"] = text
            await update.message.reply_text("💸 Бюджет:")
            context.user_data["step"] = "budget"
        elif step == "budget":
            context.user_data["budget"] = text
            await update.message.reply_text("💭 Пожелания:")
            context.user_data["step"] = "wishes"
        elif step == "wishes":
            context.user_data["wishes"] = text
            await update.message.reply_text("📲 Контакт для связи:")
            context.user_data["step"] = "contact"
        elif step == "contact":
            context.user_data["contact"] = text
            data = context.user_data
            msg = (
                f"📩 Новая заявка:\n"
                f"Дата: {data['date']}\n"
                f"Локация: {data['location']}\n"
                f"Гостей: {data['guests']}\n"
                f"Бюджет: {data['budget']}\n"
                f"Пожелания: {data['wishes']}\n"
                f"Контакт: {data['contact']}"
            )
            await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
            await update.message.reply_text("✅ Спасибо! Я скоро с вами свяжусь!")
            context.user_data.clear()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
