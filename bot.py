
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")

# Включаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот по восстановлению. Введи /stretch или /offday.")

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

# Основной запуск
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stretch", stretch))
    application.add_handler(CommandHandler("offday", offday))

    application.run_polling()

if __name__ == "__main__":
    print("Бот запущен.")
    main()
