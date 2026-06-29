"""
Callback handlers
"""

import logging
from aiogram import Router, types
from aiogram.filters import Text

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(Text(startswith="action_"))
async def handle_action_callback(callback: types.CallbackQuery):
    """Handle action callbacks"""
    action = callback.data.replace("action_", "")
    
    if action == "connect":
        await callback.message.answer("Используйте /connect для подключения")
    elif action == "check":
        await callback.message.answer("Используйте /check для проверки писем")
    elif action == "settings":
        await callback.message.answer("Используйте /settings для настроек")
    
    await callback.answer()


def register_handlers(dp):
    """Register callback handlers"""
    dp.include_router(router)
