"""
Email fetcher for IMAP
"""

import logging
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any

from bot.config import Config

logger = logging.getLogger(__name__)


class MailFetcher:
    """Fetch emails from Mail.ru via IMAP"""
    
    def __init__(self):
        self.imap_client = None
        self.email = None
        self.password = None
    
    async def connect(self, email_addr: str, password: str):
        """Connect to Mail.ru IMAP"""
        try:
            self.imap_client = imaplib.IMAP4_SSL(Config.MAIL_RU_IMAP_HOST, Config.MAIL_RU_IMAP_PORT)
            self.imap_client.login(email_addr, password)
            self.email = email_addr
            self.password = password
            logger.info(f"✅ Connected to Mail.ru IMAP for {email_addr}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to IMAP: {e}")
            return False
    
    async def fetch(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch emails from inbox"""
        try:
            self.imap_client.select('INBOX')
            status, messages = self.imap_client.search(None, 'ALL')
            
            if status != 'OK':
                logger.warning("⚠️ No emails found")
                return []
            
            email_ids = messages[0].split()[-limit:]
            emails = []
            
            for email_id in reversed(email_ids):
                try:
                    status, msg_data = self.imap_client.fetch(email_id, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    msg = email.message_from_bytes(msg_data[0][1])
                    email_info = self._parse_email(msg)
                    emails.append(email_info)
                except Exception as e:
                    logger.warning(f"⚠️ Error parsing email: {e}")
                    continue
            
            logger.info(f"✅ Fetched {len(emails)} emails")
            return emails
        except Exception as e:
            logger.error(f"❌ Error fetching emails: {e}")
            return []
    
    def _parse_email(self, msg) -> Dict[str, Any]:
        """Parse email message"""
        try:
            from_header = msg.get('From', 'Unknown')
            subject_header = msg.get('Subject', 'No Subject')
            date_header = msg.get('Date', '')
            
            from_addr = self._decode_header(from_header)
            subject = self._decode_header(subject_header)
            body = self._get_body(msg)
            
            return {
                'from': from_addr,
                'subject': subject,
                'body': body[:500] if body else '',
                'date': date_header,
                'full_message': msg
            }
        except Exception as e:
            logger.error(f"❌ Error parsing email: {e}")
            return {'from': 'Unknown', 'subject': 'Error parsing', 'body': '', 'date': ''}
    
    def _decode_header(self, header: str) -> str:
        """Decode email header"""
        try:
            decoded_parts = decode_header(header)
            decoded_string = ''
            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    decoded_string += part.decode(charset or 'utf-8', errors='ignore')
                else:
                    decoded_string += str(part)
            return decoded_string
        except Exception as e:
            logger.warning(f"⚠️ Error decoding header: {e}")
            return str(header)
    
    def _get_body(self, msg) -> str:
        """Extract email body"""
        body = ''
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    body = body.decode(charset or 'utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            body = body.decode(charset or 'utf-8', errors='ignore') if body else ''
        return body
    
    async def disconnect(self):
        """Disconnect from IMAP"""
        try:
            if self.imap_client:
                self.imap_client.close()
                self.imap_client.logout()
                logger.info("✅ Disconnected from Mail.ru IMAP")
        except Exception as e:
            logger.error(f"❌ Error disconnecting: {e}")
