"""
ID Resolver Module

Resolves Slack user IDs and channel IDs to human-readable names.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class IDResolver:
    """Resolves IDs to human-readable names."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.slack_config = config.get('slack', {})
        self._user_cache: Dict[str, str] = {}
        self._channel_cache: Dict[str, str] = {}
        
        # Known mappings from config and discovered users
        self._known_users = {
            'U06LKHPJG3W': 'hengo',  # From config
            'U059S071SSZ': 'shayg',  # Shay Tal-Gerby
            'U05J8235L06': 'shahari',  # Shahar Itzko
            'U07CMQF9PEF': 'talso',  # Tal Soffer Nachshon
            'U0UEZE475': 'gavinr',  # Gavin Rifkind
            'U09K614FQP9': 'talso',  # Tal Soffer Nachshon (same as U07CMQF9PEF)
            'U02QNEXLC3A': 'bard',  # Bar Darmon
        }
        
        self._known_channels = {
            'C0A6AMMMTFY': '#anon-cart',  # From config
        }
    
    def resolve_user_id(self, user_id: str) -> str:
        """
        Resolve Slack user ID to username.
        
        Args:
            user_id: Slack user ID (e.g., U06LKHPJG3W)
            
        Returns:
            str: Username or user ID if not found
        """
        if not user_id or not user_id.startswith('U'):
            return user_id
        
        # Check cache
        if user_id in self._user_cache:
            return self._user_cache[user_id]
        
        # Check known mappings
        if user_id in self._known_users:
            username = self._known_users[user_id]
            self._user_cache[user_id] = username
            return username
        
        # TODO: Use MCP-S Slack tools to resolve
        # For now, return the ID
        # In actual implementation, would use:
        # mcp_MCP-S-SLACK_slack__slack_get_user_profile(user_id=user_id)
        # to get the username
        
        logger.debug(f"User ID {user_id} not resolved, using ID")
        return user_id
    
    def resolve_channel_id(self, channel_id: str) -> str:
        """
        Resolve Slack channel ID to channel name.
        
        Args:
            channel_id: Slack channel ID (e.g., C0A6AMMMTFY)
            
        Returns:
            str: Channel name with # prefix or channel ID if not found
        """
        if not channel_id or not channel_id.startswith('C'):
            return channel_id
        
        # Check cache
        if channel_id in self._channel_cache:
            return self._channel_cache[channel_id]
        
        # Check known mappings
        if channel_id in self._known_channels:
            channel_name = self._known_channels[channel_id]
            self._channel_cache[channel_id] = channel_name
            return channel_name
        
        # TODO: Use MCP-S Slack tools to resolve
        # For now, return the ID
        # In actual implementation, would use:
        # mcp_MCP-S-SLACK_slack__slack_find-channel-id or list channels
        # to get the channel name
        
        logger.debug(f"Channel ID {channel_id} not resolved, using ID")
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
