"""
Mail.ru SMTP/IMAP connector
"""

import logging
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bot.config import Config

logger = logging.getLogger(__name__)


class MailConnector:
    """Mail.ru connector for SMTP/IMAP operations"""
    
    def __init__(self):
        self.smtp_client = None
        self.email = None
        self.password = None
    
    async def connect(self, email: str, password: str):
        """Connect to Mail.ru SMTP"""
        try:
            self.email = email
            self.password = password
            
            self.smtp_client = aiosmtplib.SMTP(
                hostname=Config.MAIL_RU_SMTP_HOST,
                port=Config.MAIL_RU_SMTP_PORT,
                use_tls=True
            )
            
            await self.smtp_client.connect()
            await self.smtp_client.login(email, password)
            
            logger.info(f"✅ Connected to Mail.ru SMTP for {email}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to Mail.ru: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Mail.ru"""
        try:
            if self.smtp_client:
                await self.smtp_client.quit()
                self.smtp_client = None
                logger.info("✅ Disconnected from Mail.ru SMTP")
        except Exception as e:
            logger.error(f"❌ Error disconnecting: {e}")
