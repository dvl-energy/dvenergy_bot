
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот по восстановлению. Введи /stretch или /offday.")

async def stretch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🧘‍♂️ <b>Вечерняя растяжка (15 мин)</b>\n"
        "1. Диафрагмальное дыхание — 2 мин\n"
        "2. Шея: наклоны + ухо к плечу — 10 раз / 20 сек\n"
        "3. Скрутка лёжа — 2x30 сек\n"
        "4. «Кошка-корова» — 10 раз\n"
        "5. Растяжка ягодиц и грушевидной — 30 сек/сторона\n"
        "6. Наклон к ногам — 30 сек\n"
        "7. Ноги на стене + дыхание (4/8) — 2–3 мин"
    )
    await update.message.reply_text(text, parse_mode='HTML')

async def offday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛌 <b>Полный OFF-день</b>\n"
        "✅ Прогулка на свежем воздухе — 30+ мин\n"
        "✅ Сон 8+ часов (можно дневной)\n"
        "✅ Ванна / баня / душ\n"
        "✅ Медитация или тишина — 10–30 мин\n"
        "✅ Без экрана минимум 3 часа подряд\n"
        "✅ Питание: минимум сахара, больше жиров и овощей\n"
        "✅ Чтение, отдых, живое общение\n"
        "❌ Никаких тренировок\n"
        "❌ Без кофеина после 14:00"
    )
    await update.message.reply_text(text, parse_mode='HTML')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stretch", stretch))
    app.add_handler(CommandHandler("offday", offday))
    print("Бот запущен.")
    app.run_polling()
