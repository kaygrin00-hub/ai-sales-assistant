"""
Command handlers
"""

import logging
from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards import get_main_menu
from bot.services.user import UserService
from bot.services.mail import MailService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command"""
    user_id = message.from_user.id
    user_service = UserService()
    
    user = await user_service.get_or_create_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    welcome_text = f"""🎉 Добро пожаловать в Telegram Mail Bot!

👤 Привет, {message.from_user.first_name}!

Этот бот помогает вам:
📧 Управлять почтой Mail.ru
🔔 Получать уведомления о новых письмах
⏰ Устанавливать напоминания
📊 Анализировать письма

Начните с подключения вашего Mail.ru аккаунта!"""
    
    await message.answer(welcome_text, reply_markup=get_main_menu())
    logger.info(f"✅ User {user_id} started bot")


@router.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command"""
    help_text = """📖 Справка по командам:

/start - Начать работу
/help - Эта справка
/connect - Подключить Mail.ru аккаунт
/disconnect - Отключить аккаунт
/check - Проверить новые письма
/stats - Показать статистику
/settings - Настройки

🎯 Основные возможности:

1️⃣ Подключение аккаунта
   - Используйте /connect
   - Введите пароль приложения Mail.ru
   - Разрешите доступ к почте

2️⃣ Проверка писем
   - /check для ручной проверки
   - Автоматическая проверка каждые 5 минут
   - Уведомления о новых письмах

3️⃣ Управление
   - Просмотр статистики (/stats)
   - Изменение настроек (/settings)
   - Отключение аккаунта (/disconnect)

❓ Вопросы или проблемы? Свяжитесь с разработчиком!"""
    
    await message.answer(help_text)


@router.message(Command("connect"))
async def connect_command(message: types.Message):
    """Handle /connect command"""
    user_id = message.from_user.id
    user_service = UserService()
    
    user = await user_service.get_user(user_id)
    if user and user.is_connected:
        await message.answer(
            "⚠️ Вы уже подключили аккаунт!\n\n"
            "Используйте /disconnect если хотите отключиться."
        )
        return
    
    connect_text = """📧 Подключение Mail.ru аккаунта

Для подключения вам нужен пароль приложения:

1️⃣ Перейдите на https://account.mail.ru
2️⃣ В меню выберите "Безопасность"
3️⃣ Нажмите "Пароли приложений"
4️⃣ Выберите "Telegram" и создайте пароль
5️⃣ Отправьте мне пароль в формате:
   your_email@mail.ru:password

⚠️ Пароль будет зашифрован и безопасно сохранён"""
    
    await message.answer(connect_text)
    logger.info(f"ℹ️ User {user_id} started connection process")


@router.message(Command("check"))
async def check_command(message: types.Message):
    """Handle /check command"""
    user_id = message.from_user.id
    user_service = UserService()
    
    user = await user_service.get_user(user_id)
    if not user or not user.is_connected:
        await message.answer(
            "❌ Вы не подключили аккаунт!\n\n"
            "Используйте /connect для подключения."
        )
        return
    
    await message.answer("📬 Проверяю новые письма...")
    
    mail_service = MailService()
    try:
        emails = await mail_service.fetch_emails(user_id)
        
        if not emails:
            await message.answer("✅ Новых писем нет!")
            return
        
        result_text = f"📧 Найдено писем: {len(emails)}\n\n"
        
        for email in emails[:5]:
            result_text += f"📨 От: {email.get('from', 'Unknown')}\n"
            result_text += f"   Тема: {email.get('subject', 'No subject')}\n"
            result_text += f"   Дата: {email.get('date', 'Unknown')}\n\n"
        
        if len(emails) > 5:
            result_text += f"... и ещё {len(emails) - 5} писем"
        
        await message.answer(result_text)
        logger.info(f"✅ User {user_id} checked emails: {len(emails)} found")
        
    except Exception as e:
        logger.error(f"❌ Error checking emails for user {user_id}: {e}")
        await message.answer(f"❌ Ошибка при проверке писем: {str(e)}")


@router.message(Command("stats"))
async def stats_command(message: types.Message):
    """Handle /stats command"""
    user_id = message.from_user.id
    user_service = UserService()
    
    user = await user_service.get_user(user_id)
    if not user:
        await message.answer("❌ Пользователь не найден")
        return
    
    stats_text = f"""📊 Ваша статистика:

👤 Пользователь: {user.first_name or 'Unknown'}
🔗 Статус: {'🟢 Подключен' if user.is_connected else '🔴 Не подключен'}
📧 Email: {user.email or 'Не установлен'}
📬 Всего писем: {user.total_emails or 0}
🆕 Новых писем: {user.unread_emails or 0}
📅 Дата подключения: {user.connected_at or 'N/A'}
⏰ Последняя проверка: {user.last_check_at or 'Никогда'}"""
    
    await message.answer(stats_text)


@router.message(Command("disconnect"))
async def disconnect_command(message: types.Message):
    """Handle /disconnect command"""
    user_id = message.from_user.id
    user_service = UserService()
    
    user = await user_service.get_user(user_id)
    if not user or not user.is_connected:
        await message.answer("❌ Вы не подключили аккаунт!")
        return
    
    await user_service.disconnect_user(user_id)
    await message.answer("✅ Аккаунт отключен!")
    logger.info(f"✅ User {user_id} disconnected")


@router.message(Command("settings"))
async def settings_command(message: types.Message):
    """Handle /settings command"""
    settings_text = """⚙️ Настройки:

🔔 Уведомления
💾 Хранилище
🔐 Безопасность
🌐 Язык

(Функция в разработке)"""
    
    await message.answer(settings_text)


def register_handlers(dp):
    """Register command handlers"""
    dp.include_router(router)
