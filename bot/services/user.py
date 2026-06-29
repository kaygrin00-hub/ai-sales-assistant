"""
User service
"""

import logging
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_session

logger = logging.getLogger(__name__)


class UserService:
    """User service for database operations"""
    
    async def get_user(self, user_id: int):
        """Get user by ID"""
        async with get_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def get_or_create_user(self, user_id: int, username=None, first_name=None, last_name=None):
        """Get or create user"""
        async with get_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if user:
                logger.info(f"✅ User {user_id} found")
                return user
            
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                created_at=datetime.utcnow()
            )
            
            session.add(user)
            await session.commit()
            logger.info(f"✅ User {user_id} created")
            return user
    
    async def update_user(self, user_id: int, **kwargs):
        """Update user"""
        async with get_session() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            await session.commit()
            logger.info(f"✅ User {user_id} updated")
            return user
    
    async def disconnect_user(self, user_id: int):
        """Disconnect user email account"""
        return await self.update_user(
            user_id,
            is_connected=False,
            password=None,
            email=None
        )
    
    async def update_check_time(self, user_id: int):
        """Update last check time"""
        return await self.update_user(
            user_id,
            last_check_at=datetime.utcnow()
        )
