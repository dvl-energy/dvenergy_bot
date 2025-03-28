import logging
import os
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот по восстановлению. Введи /stretch, /offday или /training.")

async def stretch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧘‍♂️ Вечерняя растяжка (15 мин):\n"
        "1. Дыхание — 2 мин\n"
        "2. Шея — 10x / 20 сек\n"
        "3. Скрутка лёжа — 2x30 сек\n"
        "4. Кошка-корова — 10 раз\n"
        "5. Ягодицы + грушевидная — 30 сек/сторона\n"
        "6. Наклон к ногам — 30 сек\n"
        "7. Ноги на стене + дыхание — 3 мин"
    )

async def offday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛌 Полный OFF-день:\n"
        "✅ Прогулка — 30+ мин\n"
        "✅ Сон 8+ ч\n"
        "✅ Ванна / баня\n"
        "✅ Без экрана 3 часа\n"
        "✅ Еда: без сахара, больше жиров\n"
        "✅ Медитация / отдых\n"
        "❌ Никаких тренировок\n"
        "❌ Кофеин после 14:00"
    )

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day = datetime.now().weekday()
    if day == 0:
        await update.message.reply_text(
            "🏋️‍♂️ <b>Тренировка A</b>\n"
            "- Подтягивания / тяга блока — 3x8–10\n"
            "- Болгарские приседы — 3x8\n"
            "- Жим гантелей лёжа — 3x10\n"
            "- Гиперэкстензия — 3x15\n"
            "- Тяга гантели в наклоне — 3x10", parse_mode='HTML')
    elif day == 3:
        await update.message.reply_text(
            "🏋️‍♂️ <b>Тренировка B</b>\n"
            "- Жим гантелей стоя — 3x8\n"
            "- Гоблет-присед — 3x10\n"
            "- Ягодичный мостик — 3x15\n"
            "- Подъём ног в висе — 3x15\n"
            "- Интервальный вело 30/30 — 10 мин", parse_mode='HTML')
    else:
        await update.message.reply_text("📅 Сегодня не силовой день. Отдыхай или нажми /offday")

async def send_evening_reminder(context: CallbackContext):
    await context.bot.send_message(chat_id=context.job.chat_id,
                                   text="🧘‍♂️ Напоминание: сделай вечернюю растяжку! ➡ /stretch")

# Запуск
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stretch", stretch))
    application.add_handler(CommandHandler("offday", offday))
    application.add_handler(CommandHandler("training", training))

    # Планирование напоминания на 21:00 по МСК
    moscow_utc_offset = 3  # Moscow = UTC+3
    now_utc = datetime.utcnow()
    now_msk = now_utc + timedelta(hours=moscow_utc_offset)
    reminder_time = time(21, 0)
    delta = datetime.combine(now_msk.date(), reminder_time) - now_msk
    if delta.total_seconds() < 0:
        delta += timedelta(days=1)

    application.job_queue.run_repeating(
        send_evening_reminder,
        interval=86400,
        first=delta,
        chat_id=os.getenv("CHAT_ID")  # ты можешь временно заменить это на свой chat_id
    )

    print("Бот запущен.")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
