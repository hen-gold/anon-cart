"""
ID Resolver Module

Resolves Slack user IDs and channel IDs to human-readable names.
Uses Slack Web API when not in known mappings.
"""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def _slack_client():
    """Return Slack WebClient if token set, else None."""
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        return None
    try:
        from slack_sdk import WebClient
        return WebClient(token=token)
    except ImportError:
        return None


class IDResolver:
    """Resolves IDs to human-readable names."""

    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.slack_config = config.get("slack", {})
        self._user_cache: Dict[str, str] = {}
        self._channel_cache: Dict[str, str] = {}

        self._known_users = {
            "U06LKHPJG3W": "hengo",
            "U059S071SSZ": "shayg",
            "U05J8235L06": "shahari",
            "U07CMQF9PEF": "talso",
            "U0UEZE475": "gavinr",
            "U09K614FQP9": "talso",
            "U02QNEXLC3A": "bard",
        }

        self._known_channels = {
            "C0A6AMMMTFY": "#anon-cart",
        }

    def resolve_user_id(self, user_id: str) -> str:
        """
        Resolve Slack user ID to username (display name or real name).
        Uses known mappings, then Slack Web API users.info.
        """
        if not user_id or not user_id.startswith("U"):
            return user_id

        if user_id in self._user_cache:
            return self._user_cache[user_id]
        if user_id in self._known_users:
            name = self._known_users[user_id]
            self._user_cache[user_id] = name
            return name

        client = _slack_client()
        if client:
            try:
                r = client.users_info(user=user_id)
                if r.get("ok") and r.get("user"):
                    profile = r["user"].get("profile", {}) or {}
                    name = profile.get("display_name") or profile.get("real_name") or r["user"].get("name") or user_id
                    self._user_cache[user_id] = name
                    return name
            except Exception as e:
                logger.debug(f"users.info failed for {user_id}: {e}")
        return user_id

    def resolve_channel_id(self, channel_id: str) -> str:
        """
        Resolve Slack channel ID to channel name.
        Uses known mappings, then Slack Web API conversations.info.
        """
        if not channel_id or not channel_id.startswith("C"):
            return channel_id

        if channel_id in self._channel_cache:
            return self._channel_cache[channel_id]
        if channel_id in self._known_channels:
            name = self._known_channels[channel_id]
            self._channel_cache[channel_id] = name
            return name

        client = _slack_client()
        if client:
            try:
                r = client.conversations_info(channel=channel_id)
                if r.get("ok") and r.get("channel"):
                    name = r["channel"].get("name", channel_id)
                    self._channel_cache[channel_id] = "#" + name if not name.startswith("#") else name
                    return self._channel_cache[channel_id]
            except Exception as e:
                logger.debug(f"conversations.info failed for {channel_id}: {e}")
        return channel_id
    
    def resolve_user_ids_in_text(self, text: str) -> str:
        """
        Resolve all user IDs in text to usernames.
        
        Args:
            text: Text that may contain user IDs
            
        Returns:
            str: Text with user IDs replaced by usernames
        """
        import re
        # Pattern to match Slack user IDs: U followed by alphanumeric
        pattern = r'U[A-Z0-9]{10,}'
        
        def replace_user_id(match):
            user_id = match.group(0)
            return self.resolve_user_id(user_id)
        
        return re.sub(pattern, replace_user_id, text)
    
    def resolve_channel_ids_in_text(self, text: str) -> str:
        """
        Resolve all channel IDs in text to channel names.
        
        Args:
            text: Text that may contain channel IDs
            
        Returns:
            str: Text with channel IDs replaced by channel names
        """
        import re
        # Pattern to match Slack channel IDs: C followed by alphanumeric
        pattern = r'C[A-Z0-9]{10,}'
        
        def replace_channel_id(match):
            channel_id = match.group(0)
            return self.resolve_channel_id(channel_id)
        
        return re.sub(pattern, replace_channel_id, text)
    
    def resolve_all_ids(self, text: str) -> str:
        """
        Resolve all user and channel IDs in text.
        
        Args:
            text: Text that may contain user and channel IDs
            
        Returns:
            str: Text with all IDs replaced by names
        """
        text = self.resolve_user_ids_in_text(text)
        text = self.resolve_channel_ids_in_text(text)
        return text
