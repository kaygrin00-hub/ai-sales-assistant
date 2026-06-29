"""
Email analyzer for content analysis
"""

import logging
import re
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class MailAnalyzer:
    """Analyze emails for content, importance, etc."""
    
    URGENT_KEYWORDS = ['urgent', 'срочно', 'важно', 'critical', 'asap', 'необходимо']
    SPAM_KEYWORDS = ['buy now', 'click here', 'unsubscribe', 'promotion', 'sale']
    
    async def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze single email"""
        try:
            subject = email.get('subject', '')
            body = email.get('body', '')
            
            importance = self._detect_importance(subject, body)
            is_spam = self._detect_spam(subject, body)
            keywords = self._extract_keywords(subject, body)
            priority = self._calculate_priority(importance, is_spam, subject)
            
            return {
                **email,
                'importance': importance,
                'is_spam': is_spam,
                'keywords': keywords,
                'priority': priority,
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error analyzing email: {e}")
            return email
    
    async def analyze_batch(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze batch of emails"""
        analyzed = []
        for email in emails:
            analyzed_email = await self.analyze(email)
            analyzed.append(analyzed_email)
        return analyzed
    
    def _detect_importance(self, subject: str, body: str) -> str:
        """Detect email importance"""
        text = (subject + ' ' + body).lower()
        if any(keyword in text for keyword in self.URGENT_KEYWORDS):
            return 'high'
        if re.search(r'\[urgent\]|\[важно\]|!!!', subject, re.IGNORECASE):
            return 'high'
        if re.search(r'\[low\]|\[info\]', subject, re.IGNORECASE):
            return 'low'
        return 'normal'
    
    def _detect_spam(self, subject: str, body: str) -> bool:
        """Detect spam email"""
        text = (subject + ' ' + body).lower()
        spam_count = sum(1 for keyword in self.SPAM_KEYWORDS if keyword in text)
        if re.search(r'(verify|confirm|click).*account', text):
            spam_count += 2
        if re.search(r'congratulations.*won|claim.*prize', text, re.IGNORECASE):
            spam_count += 3
        return spam_count >= 2
    
    def _extract_keywords(self, subject: str, body: str) -> List[str]:
        """Extract keywords from email"""
        words = re.findall(r'\b\w{4,}\b', (subject + ' ' + body).lower())
        common_words = {'that', 'this', 'from', 'with', 'have', 'will', 'your', 'have'}
        keywords = [w for w in set(words) if w not in common_words]
        return keywords[:5]
    
    def _calculate_priority(self, importance: str, is_spam: bool, subject: str) -> int:
        """Calculate priority score (1-10)"""
        priority = 5
        if importance == 'high':
            priority += 3
        elif importance == 'low':
            priority -= 2
        if is_spam:
            priority -= 4
        if len(subject) > 50:
            priority += 1
        return max(1, min(10, priority))
