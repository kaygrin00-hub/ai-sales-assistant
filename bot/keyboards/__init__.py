"""
Keyboards package
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📧 Подключить"),
                KeyboardButton(text="📬 Проверить"),
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="⚙️ Настройки"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_connect_menu() -> InlineKeyboardMarkup:
    """Get connect menu keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Как подключить?", callback_data="action_connect_help")],
            [InlineKeyboardButton(text="Уже подключен", callback_data="action_connect_done")],
        ]
    )


def get_email_menu() -> InlineKeyboardMarkup:
    """Get email menu keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Прочитать", callback_data="action_read_email")],
            [InlineKeyboardButton(text="🔔 Напомнить позже", callback_data="action_remind_email")],
            [InlineKeyboardButton(text="📁 Переместить", callback_data="action_move_email")],
        ]
    )
