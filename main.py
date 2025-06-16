from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

BOT_TOKEN = "7927069416:AAFEOCMfd3vvtoJeUmbB8nStaSC6dwNSECA"  # Ваш токен
ADMIN_ID = 902984899  # Ваш Telegram ID

# Шаги анкеты
NAME, DATE, LOCATION, GUESTS, PHONE = range(5)

# Старт при входе
async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👰‍♀️ Вас приветствует свадебное агентство Светланы Мамедовой \"MS\"

        
