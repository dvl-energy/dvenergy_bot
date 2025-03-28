import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TRAINING_A = [
    "Подтягивания / тяга блока — 3x8–10",
    "Болгарские приседы — 3x8",
    "Жим гантелей лёжа — 3x10",
    "Гиперэкстензия — 3x15",
    "Тяга гантели в наклоне — 3x10"
]

TRAINING_B = [
    "Жим гантелей стоя — 3x8",
    "Гоблет-присед — 3x10",
    "Ягодичный мостик — 3x15",
    "Подъём ног в висе — 3x15",
    "Интервальный вело 30/30 — 10 мин"
]

def get_training_keyboard(training_list, completed):
    keyboard = []
    for i, item in enumerate(training_list):
        label = f"✅ {item}" if i in completed else f"⬜ {item}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"training_{i}")])
    return InlineKeyboardMarkup(keyboard)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот по восстановлению. Введи /stretch, /offday или /training.")

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day = datetime.now().weekday()
    if day == 0:
        await training_a(update, context)
    elif day == 3:
        await training_b(update, context)
    else:
        await update.message.reply_text("📅 Сегодня не силовой день. Отдыхай или нажми /offday")

async def training_a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["training_type"] = "A"
    context.user_data["completed"] = set()
    keyboard = get_training_keyboard(TRAINING_A, set())
    await update.message.reply_text("🏋️‍♂️ Тренировка A. Отмечай выполненные:", reply_markup=keyboard)

async def training_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["training_type"] = "B"
    context.user_data["completed"] = set()
    keyboard = get_training_keyboard(TRAINING_B, set())
    await update.message.reply_text("🏋️‍♂️ Тренировка B. Отмечай выполненные:", reply_markup=keyboard)

async def handle_training_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.split("_")[1])

    training_type = context.user_data.get("training_type")
    completed = context.user_data.get("completed", set())

    if index in completed:
        completed.remove(index)
    else:
        completed.add(index)

    context.user_data["completed"] = completed

    training_list = TRAINING_A if training_type == "A" else TRAINING_B
    keyboard = get_training_keyboard(training_list, completed)

    if len(completed) == len(training_list):
        await query.edit_message_text("✅ Тренировка завершена! Красавчик 💪")
    else:
        await query.edit_message_reply_markup(reply_markup=keyboard)

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("training_a", training_a))
    app.add_handler(CommandHandler("training_b", training_b))
    app.add_handler(CallbackQueryHandler(handle_training_callback, pattern="^training_"))

    print("Бот с тренировками запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
