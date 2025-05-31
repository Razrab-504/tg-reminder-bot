from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio


from src.keyboards.inline import remind_inline_kbd, check_remainders, delete_remainders
from src.keyboards.inline import start_kbd

from src.BD.bd_for_users import init_db, create_db, get_user_reminders, delete_reminder, get_all_reminders

class Writing(StatesGroup):
    writing = State()

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привет! 👋 Я бот-напоминалка.\n Нажмите на одну из следующих кнопок", reply_markup=start_kbd)


# Реакция на кнопку remind
@user_private_router.callback_query(F.data == "write_reminder")
async def remind_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "📝 Отлично! Давай создадим напоминание.\n\n"
        "Напиши мне сообщение в таком формате:\n\n"
        "<b>Название текста | Текст напоминания | дата и время</b>\n"
        "📌 Пример: <i>Звонок | Позвонить маме | 2025-05-24 18:30</i>",
        parse_mode="HTML",
        reply_markup=remind_inline_kbd,
    )


# Записывашешь напоминалку
@user_private_router.callback_query(F.data == "write")
async def writing_cmd(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "✍️ Напиши напоминание в формате:\n"
        "<название текста> | <текст> | <ГГГГ-ММ-ДД ЧЧ:ММ>\n\n"
        "Пример: Звонок | Позвонить маме | 2025-05-24 18:30"
    )
    await state.set_state(Writing.writing)
    await callback.answer()
    

# Сохраняешь напоминалку в БД
@user_private_router.message(Writing.writing)
async def procesing_cmd(message: Message, state: FSMContext):
    text = message.text

    parts = list(map(str.strip, text.split("|")))

    if len(parts) != 3:
        await message.answer(
            "❗ Формат неправильный. Используй:\n"
            "название | текст | дата и время\n\n"
            "Пример: Звонок | Позвонить маме | 2025-05-24 18:30"
        )
        return

    title, content, reminder_datetime = parts

    try:
        dt = datetime.strptime(reminder_datetime, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("❗ Неверный формат даты и времени. Используй: ГГГГ-ММ-ДД ЧЧ:ММ\nПример: 2025-05-24 18:30")
        return

    init_db()
    create_db(
        user_id=message.from_user.id,
        name=title,
        text=content,
        remind_at=dt.strftime("%Y-%m-%d %H:%M")
    )


    await message.answer(
        f"✅ Напоминание сохранено!\n\n"
        f"📌 <b>{title}</b>\n📝 {content}\n🕒 {dt.strftime('%Y-%m-%d %H:%M')}",
        parse_mode="HTML"
    )
    await state.clear()

# доствет кнопки
@user_private_router.callback_query(F.data == "check_reminder")
async def show_reminder_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    reminders = get_user_reminders(user_id)
    
    kbd = check_remainders(reminders)
    
    await callback.message.answer("Ваши напоминания:", reply_markup=kbd)
    await callback.answer()


# Показывает текст в напоминаниях
@user_private_router.callback_query(F.data.startswith('reminder_'))
async def reminder_callback(callback: CallbackQuery):
    reminder_id = callback.data.split("_")[1]
    reminders = get_user_reminders(callback.from_user.id)

    reminder = next((r for r in reminders if str(r[0]) == reminder_id), None)
    if reminder is None:
        await callback.message.answer("Напоминание не найдено")
        return

    id_, name, some_id, text, remind_at = reminder

    await callback.message.answer(f"Напоминание: {name}\nТекст: {text}\nВремя: {remind_at}")


# доствет кнопки для выбора какую удалить
@user_private_router.callback_query(F.data == "delete_reminder")
async def show_reminder_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    reminders = get_user_reminders(user_id)
    
    kbd = delete_remainders(reminders)
    
    await callback.message.answer("Выберите напоминание которое хотите удалить:", reply_markup=kbd)
    await callback.answer()
    

@user_private_router.callback_query(F.data.startswith('delete_reminder'))
async def delete_cmd(callback: CallbackQuery):
    reminder_id = callback.data.split("_")[2]
    delete_reminder(reminder_id=reminder_id)
    
    await callback.message.answer("Эта запись была удалена")
    await callback.answer()
    
