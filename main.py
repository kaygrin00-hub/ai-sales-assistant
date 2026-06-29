#!/usr/bin/env python3
"""
Telegram Mail Bot - Main Entry Point
"""

import asyncio
import logging
from bot.core import TelegramMailBot


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )


async def main():
    """Start the bot"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting Telegram Mail Bot...")
    
    bot = TelegramMailBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("⛔ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
    finally:
        await bot.stop()
        logger.info("✅ Bot shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
