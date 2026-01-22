"""
Changelog Module

Manages the live changelog file with real-time updates.
"""

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class Changelog:
    """Manages the live changelog."""
    
    def __init__(self, config):
        """Initialize with configuration."""
        self.config = config
        self.changelog_file = Path(config.get('reporting', {}).get('changelog_file', 'conductor/CHANGELOG.md'))
        
    def add_entries(self, changes):
        """
        Add entries to the changelog.
        
        Args:
            changes: List of change dictionaries
        """
        if not changes:
            return
        
        if not self.changelog_file.exists():
            logger.warning(f"Changelog file not found: {self.changelog_file}")
            return
        
        try:
            # Read current changelog
            with open(self.changelog_file, 'r') as f:
                content = f.read()
            
            # Generate new entries
            new_entries = self._format_entries(changes)
            
            # Insert after [Unreleased] section
            if '## [Unreleased]' in content:
                # Insert after [Unreleased] header
                insert_pos = content.find('## [Unreleased]') + len('## [Unreleased]')
                if content[insert_pos:insert_pos+2] != '\n\n':
                    new_entries = '\n\n' + new_entries
                content = content[:insert_pos] + new_entries + content[insert_pos:]
            else:
                # Add [Unreleased] section if not present
                content = f"## [Unreleased]\n\n{new_entries}\n\n---\n\n{content}"
            
            # Write back
            with open(self.changelog_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Added {len(changes)} entries to changelog")
            
        except Exception as e:
            logger.error(f"Error updating changelog: {e}")
    
    def _format_entries(self, changes):
        """
        Format change entries for changelog.
        
        Args:
            changes: List of change dictionaries
            
        Returns:
            str: Formatted changelog entries
        """
        entries = []
        
        for change in changes:
            timestamp = change.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M'))
            change_type = change.get('type', 'Unknown')
            entry = f"### {timestamp} - {change_type}\n"
            
            # Add details
            if change.get('repository'):
                entry += f"- **Repository**: {change['repository']}\n"
            if change.get('issue'):
                entry += f"- **Issue**: {change['issue']}\n"
            if change.get('commit'):
                entry += f"- **Commit**: {change['commit']}\n"
            if change.get('change'):
                entry += f"- **Change**: {change['change']}\n"
            if change.get('context_updated'):
                entry += f"- **Context Updated**: {change['context_updated']}\n"
            if change.get('impact'):
                entry += f"- **Impact**: {change['impact']}\n"
            
            entry += "\n"
            entries.append(entry)
        
        return ''.join(entries)
    
    def get_recent_changes(self, days=7):
        """
        Get recent changes from changelog.
        
        Args:
            days: Number of days to look back
            
        Returns:
            list: Recent change entries
        """
        if not self.changelog_file.exists():
            return []
        
        try:
            with open(self.changelog_file, 'r') as f:
                content = f.read()
            
            # Parse and return recent entries
            # TODO: Implement parsing logic
            
            return []
            
        except Exception as e:
            logger.error(f"Error reading changelog: {e}")
            return []
