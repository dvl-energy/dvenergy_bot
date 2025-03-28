import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Список шагов растяжки
STRETCH_STEPS = [
    "1. Дыхание — 2 мин",
    "2. Шея — 10x / 20 сек",
    "3. Скрутка лёжа — 2x30 сек",
    "4. Кошка-корова — 10 раз",
    "5. Ягодицы + грушевидная — 30 сек/сторона",
    "6. Наклон к ногам — 30 сек",
    "7. Ноги на стене + дыхание — 3 мин"
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот по восстановлению. Введи /stretch, /offday или /training.")

# Команда /stretch с чеклистом
async def stretch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"⬜ {step}", callback_data=f"stretch_{i}")]
        for i, step in enumerate(STRETCH_STEPS)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧘‍♂️ Вечерняя растяжка (отмечай выполненные):", reply_markup=reply_markup)

# Обработка кнопок чеклиста
async def handle_stretch_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.split("_")[1])

    # Обновляем состояние кнопок
    keyboard = []
    for i, step in enumerate(STRETCH_STEPS):
        if i == index:
            label = f"✅ {step}"
        else:
            if "✅" in query.message.reply_markup.inline_keyboard[i][0].text:
                label = query.message.reply_markup.inline_keyboard[i][0].text
            else:
                label = f"⬜ {step}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"stretch_{i}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stretch", stretch))
    app.add_handler(CallbackQueryHandler(handle_stretch_callback, pattern="^stretch_"))

    print("Бот запущен с интерактивным чеклистом для растяжки.")
    app.run_polling()

if __name__ == "__main__":
    main()
