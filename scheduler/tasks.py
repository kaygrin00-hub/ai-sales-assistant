"""
Background scheduler tasks
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.config import Config

logger = logging.getLogger(__name__)


def init_scheduler() -> AsyncIOScheduler:
    """Initialize scheduler"""
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        check_emails_task,
        IntervalTrigger(minutes=Config.CHECK_INTERVAL_MINUTES),
        name='check_emails',
        replace_existing=True
    )
    
    scheduler.add_job(
        send_reminders_task,
        IntervalTrigger(minutes=1),
        name='send_reminders',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("✅ Scheduler started")
    return scheduler


async def check_emails_task():
    """Periodic task to check emails"""
    logger.info("📧 Checking emails for all users...")
    try:
        pass
    except Exception as e:
        logger.error(f"❌ Error checking emails: {e}")


async def send_reminders_task():
    """Periodic task to send reminders"""
    logger.info("⏰ Checking reminders...")
    try:
        pass
    except Exception as e:
        logger.error(f"❌ Error sending reminders: {e}")
