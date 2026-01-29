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

    def __init__(self, config, project_root=None):
        """Initialize with configuration and optional project root for path resolution."""
        self.config = config
        rel = config.get("reporting", {}).get("changelog_file", "conductor/CHANGELOG.md")
        self.changelog_file = (Path(project_root) / rel) if project_root else Path(rel)
        
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
        Get recent changes from changelog by parsing ### timestamp - Type entries.

        Args:
            days: Number of days to look back

        Returns:
            list: List of dicts with keys: timestamp, type, repository, issue, commit, change, context_updated, impact, raw_text
        """
        if not self.changelog_file.exists():
            return []

        try:
            with open(self.changelog_file, "r") as f:
                content = f.read()

            from datetime import datetime, timedelta
            cutoff = (datetime.now() - timedelta(days=days)).date()
            entries = []
            current = None
            lines_buf = []

            for line in content.split("\n"):
                if line.strip().startswith("### ") and " - " in line:
                    if current is not None:
                        entries.append(current)
                    # Parse "### 2026-01-20 12:00 - Jira Update"
                    rest = line.strip()[4:].strip()
                    if " - " in rest:
                        ts_part, type_part = rest.split(" - ", 1)
                        ts_part = ts_part.strip()
                        type_part = type_part.strip()
                        try:
                            dt = datetime.strptime(ts_part[:10], "%Y-%m-%d")
                            if dt.date() >= cutoff:
                                current = {
                                    "timestamp": ts_part,
                                    "type": type_part,
                                    "repository": None,
                                    "issue": None,
                                    "commit": None,
                                    "change": None,
                                    "context_updated": None,
                                    "impact": None,
                                    "raw_text": line + "\n",
                                }
                                lines_buf = [line]
                            else:
                                current = None
                        except ValueError:
                            current = None
                    else:
                        current = None
                elif current is not None and (line.startswith("- **") or line.strip() == ""):
                    current["raw_text"] = current.get("raw_text", "") + line + "\n"
                    if "**Repository**:" in line:
                        current["repository"] = line.split(":", 1)[-1].strip()
                    elif "**Issue**:" in line:
                        current["issue"] = line.split(":", 1)[-1].strip()
                    elif "**Commit**:" in line:
                        current["commit"] = line.split(":", 1)[-1].strip()
                    elif "**Change**:" in line:
                        current["change"] = line.split(":", 1)[-1].strip()
                    elif "**Context Updated**:" in line:
                        current["context_updated"] = line.split(":", 1)[-1].strip()
                    elif "**Impact**:" in line:
                        current["impact"] = line.split(":", 1)[-1].strip()
                else:
                    if current is not None and line.strip() and not line.startswith("## ") and not line.startswith("# "):
                        current["raw_text"] = current.get("raw_text", "") + line + "\n"
                    elif line.strip().startswith("## ") or line.strip().startswith("# "):
                        if current is not None:
                            entries.append(current)
                        current = None

            if current is not None:
                entries.append(current)
            return entries

        except Exception as e:
            logger.error(f"Error reading changelog: {e}")
            return []
