import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from aiogram import Bot
from src.BD.bd_for_users import get_all_reminders

scheduler = AsyncIOScheduler()

async def send_reminder(bot: Bot, user_id: int, name: str, text: str):
    try:
        await bot.send_message(user_id, f"🔔 Напоминание: <b>{name}</b>\n\n{text}", parse_mode="HTML")
        print(f"Отправлено напоминание пользователю {user_id}")
    except Exception as e:
        print(f"Не удалось отправить напоминание {user_id}: {e}")

def schedule_all_reminders(bot: Bot, scheduler: AsyncIOScheduler):
    reminders = get_all_reminders()
    print(f"Найдено напоминаний: {len(reminders)}")
    
    for reminder in reminders:
        reminder_id, name, user_id, text, remind_at = reminder
        
        try:
            remind_time = datetime.strptime(remind_at, "%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"Ошибка в дате напоминания id={reminder_id}: {e}")
            continue
        
        # Если напоминание уже прошло, пропускаем
        if remind_time <= datetime.now():
            print(f"Напоминание id={reminder_id} уже просрочено, пропускаем")
            continue
        
        print(f"Запланировано напоминание id={reminder_id} на {remind_time}")

        # Добавляем асинхронную задачу напрямую в планировщик
        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=remind_time,
            args=[bot, user_id, name, text],  # Передаем аргументы в функцию
            id=f"reminder_{reminder_id}",
            misfire_grace_time=60 * 60  # Даем 1 час на выполнение, если сервер упал
        )