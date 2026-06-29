"""
Core bot class
"""

import logging
import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.config import Config
from bot.handlers import register_handlers
from db.session import init_db
from scheduler.tasks import init_scheduler

logger = logging.getLogger(__name__)


class TelegramMailBot:
    """Main bot class"""
    
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.storage = MemoryStorage()
        self.scheduler = None
    
    async def start(self):
        """Start the bot"""
        # Initialize database
        logger.info("📊 Initializing database...")
        await init_db()
        
        # Create bot and dispatcher
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher(storage=self.storage)
        
        # Register handlers
        logger.info("📝 Registering handlers...")
        register_handlers(self.dp)
        
        # Set bot commands
        await self._set_commands()
        
        # Initialize scheduler
        logger.info("⏰ Initializing scheduler...")
        self.scheduler = init_scheduler()
        
        # Start polling
        logger.info("🔄 Starting polling...")
        try:
            await self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())
        except Exception as e:
            logger.error(f"❌ Polling error: {e}")
            raise
    
    async def stop(self):
        """Stop the bot"""
        if self.scheduler:
            self.scheduler.shutdown()
            logger.info("⏰ Scheduler stopped")
        
        if self.bot:
            await self.bot.session.close()
            logger.info("🔌 Bot session closed")
    
    async def _set_commands(self):
        """Set bot commands"""
        commands = [
            BotCommand(command="start", description="🚀 Start the bot"),
            BotCommand(command="help", description="📖 Get help"),
            BotCommand(command="connect", description="📧 Connect Mail.ru account"),
            BotCommand(command="disconnect", description="🔓 Disconnect account"),
            BotCommand(command="check", description="📬 Check emails"),
            BotCommand(command="stats", description="📊 Show statistics"),
            BotCommand(command="settings", description="⚙️ Settings"),
        ]
        
        await self.bot.set_my_commands(commands)
        logger.info("✅ Bot commands set")
