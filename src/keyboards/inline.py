from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✍️ /remind",
                callback_data="write_reminder"
            ),
            InlineKeyboardButton(
                text = "🔍 /check_remind",
                callback_data="check_reminder"
            ),
            InlineKeyboardButton(
                text="🗑 /delete_remind",
                callback_data="delete_reminder"
            )
        ]
    ]
)

remind_inline_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✍️ Написать напоминание",
                callback_data="write"
            )
        ]
    ]
)

remind_check_inline_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✍️ Удалить напоминания",
                callback_data="delete_reminder"
            )
        ]
    ]
)



def check_remainders(reminders):
    buttons = []
    for reminder_id, reminder_name, user_id, reminder_text, reminder_date in reminders:
        buttons.append([InlineKeyboardButton(text=reminder_name, callback_data=f"reminder_{reminder_id}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def delete_remainders(reminders):
    buttons = []
    for reminder_id, reminder_name, user_id, reminder_text, reminder_date in reminders:
        buttons.append([InlineKeyboardButton(text=reminder_name, callback_data=f"delete_reminder_{reminder_id}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard