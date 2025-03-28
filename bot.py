
import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from datetime import datetime

TOKEN = os.getenv("TOKEN")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN", "https://your-app-name.onrender.com")
PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
bot_app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

TRAINING_A = [
    "Подтягивания / тяга блока — 3x8–10",
    "Болгарские приседы — 3x8",
    "Жим гантелей лёжа — 3x10",
    "Гиперэкстензия — 3x15",
    "Тяга гантели в наклоне — 3x10",
]

TRAINING_B = [
    "Жим гантелей стоя — 3x8",
    "Гоблет-присед — 3x10",
    "Ягодичный мостик — 3x15",
    "Подъём ног в висе — 3x15",
    "Интервальный вело 30/30 — 10 мин",
]

STRETCH_LIST = [
    "Шея и плечи — 2 мин",
    "Грудной отдел — 2 мин",
    "Поясница лёжа — 2 мин",
    "Бёдра и таз — 2 мин",
    "Икры и стопы — 2 мин",
]

OFFDAY_LIST = [
    "Прогулка на свежем воздухе — 30 мин",
    "Дыхание 4-7-8 — 5 мин",
    "Контрастный душ или баня",
    "Отказ от гаджетов 1 час до сна",
    "Планы и цели на завтра — 3 мин",
]

user_logs = {}

def get_training_keyboard(training_list, completed):
    keyboard = []
    for i, item in enumerate(training_list):
        label = f"✅ {item}" if i in completed else f"⬜ {item}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"training_{i}")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("⚡ /start вызван")
    await update.message.reply_text("Привет! Я твой бот. Введи /training, /training_a или /training_b")

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

async def stretch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"⬜ {item}", callback_data=f"stretch_{i}")] for i, item in enumerate(STRETCH_LIST)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧘 Вечерняя растяжка:", reply_markup=reply_markup)

async def offday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"⬜ {item}", callback_data=f"offday_{i}")] for i, item in enumerate(OFFDAY_LIST)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌿 Полный OFF-день. Отмечай выполненное:", reply_markup=reply_markup)

async def handle_checklist_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("stretch"):
        items = STRETCH_LIST
        prefix = "stretch"
    elif data.startswith("offday"):
        items = OFFDAY_LIST
        prefix = "offday"
    else:
        return

    index = int(data.split("_")[1])
    session_key = f"{prefix}_done"
    done = context.user_data.get(session_key, set())

    if index in done:
        done.remove(index)
    else:
        done.add(index)

    context.user_data[session_key] = done
    keyboard = [[InlineKeyboardButton(f"✅ {item}" if i in done else f"⬜ {item}", callback_data=f"{prefix}_{i}")] for i, item in enumerate(items)]
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Напиши упражнение и результат (пример: Жим гантелей 24x10)")
    context.user_data["logging"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("logging"):
        user_id = update.effective_user.id
        msg = update.message.text
        user_logs.setdefault(user_id, []).append(msg)
        await update.message.reply_text(f"✅ Записано: {msg}")
        context.user_data["logging"] = False

@app.on_event("startup")
async def startup():
    logger.info("🚀 Запуск Telegram Webhook")
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("training", training))
    bot_app.add_handler(CommandHandler("training_a", training_a))
    bot_app.add_handler(CommandHandler("training_b", training_b))
    bot_app.add_handler(CallbackQueryHandler(handle_training_callback, pattern="^training_"))
    bot_app.add_handler(CommandHandler("stretch", stretch))
    bot_app.add_handler(CommandHandler("offday", offday))
    bot_app.add_handler(CommandHandler("log", log_command))
    bot_app.add_handler(CallbackQueryHandler(handle_checklist_callback, pattern="^(stretch|offday)_"))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(f"{WEBHOOK_DOMAIN}/webhook")

@app.post("/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}
