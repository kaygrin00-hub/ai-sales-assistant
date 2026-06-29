"""
Configuration for the bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
    
    # Mail.ru SMTP
    MAIL_RU_SMTP_HOST = os.getenv("MAIL_RU_SMTP_HOST", "smtp.mail.ru")
    MAIL_RU_SMTP_PORT = int(os.getenv("MAIL_RU_SMTP_PORT", "465"))
    MAIL_RU_IMAP_HOST = os.getenv("MAIL_RU_IMAP_HOST", "imap.mail.ru")
    MAIL_RU_IMAP_PORT = int(os.getenv("MAIL_RU_IMAP_PORT", "993"))
    MAIL_RU_DEFAULT_EMAIL = os.getenv("MAIL_RU_DEFAULT_EMAIL", "")
    MAIL_RU_DEFAULT_PASSWORD = os.getenv("MAIL_RU_DEFAULT_PASSWORD", "")
    
    # Application
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TIMEZONE = os.getenv("TIMEZONE", "Europe/Moscow")
    
    # Features
    ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "True").lower() == "true"
    ENABLE_REMINDERS = os.getenv("ENABLE_REMINDERS", "True").lower() == "true"
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
    
    # Security
    ALLOWED_USERS = [
        int(uid.strip()) 
        for uid in os.getenv("ALLOWED_USERS", "").split(",")
        if uid.strip()
    ] if os.getenv("ALLOWED_USERS") else []
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL not set")
        return True


# Validate on import
Config.validate()
