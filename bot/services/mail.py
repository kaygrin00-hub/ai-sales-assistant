"""
Mail service
"""

import logging
from typing import List, Dict, Any

from mail.connector import MailConnector
from mail.fetcher import MailFetcher
from mail.analyzer import MailAnalyzer
from bot.services.user import UserService

logger = logging.getLogger(__name__)


class MailService:
    """Mail service for email operations"""
    
    def __init__(self):
        self.connector = MailConnector()
        self.fetcher = MailFetcher()
        self.analyzer = MailAnalyzer()
        self.user_service = UserService()
    
    async def fetch_emails(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch emails for user"""
        try:
            user = await self.user_service.get_user(user_id)
            if not user or not user.is_connected:
                logger.warning(f"⚠️ User {user_id} is not connected")
                return []
            
            await self.connector.connect(user.email, user.password)
            emails = await self.fetcher.fetch(limit=limit)
            analyzed = await self.analyzer.analyze_batch(emails)
            await self.user_service.update_check_time(user_id)
            
            logger.info(f"✅ Fetched {len(analyzed)} emails for user {user_id}")
            return analyzed
            
        except Exception as e:
            logger.error(f"❌ Error fetching emails for user {user_id}: {e}")
            return []
        finally:
            await self.connector.disconnect()
