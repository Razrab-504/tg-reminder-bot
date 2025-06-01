import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from src.BD.bd_for_users import init_db
from src.handlers.user_privat import user_private_router
from src.reminder_scheduler.reminder_scheduler import schedule_all_reminders

TOKEN = "your_token"

# Глобальный планировщик
scheduler = AsyncIOScheduler()

async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    print("Бот запущен")
    try:
        schedule_all_reminders(bot, scheduler)
        scheduler.start()
        print("Планировщик напоминаний запущен")
    except Exception as e:
        print(f"Ошибка при запуске планировщика: {e}")

async def on_shutdown():
    """Действия при остановке бота"""
    print("Остановка бота...")
    if scheduler.running:
        scheduler.shutdown()
        print("Планировщик остановлен")

async def main():
    init_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(user_private_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
