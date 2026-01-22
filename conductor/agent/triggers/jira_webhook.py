"""
Jira Webhook Handler

Handles Jira webhook events for issue update monitoring.
"""

import logging
import json

logger = logging.getLogger(__name__)


def handle_jira_webhook(payload):
    """
    Handle Jira webhook payload.
    
    Args:
        payload: Jira webhook payload
        
    Returns:
        dict: Processing result
    """
    try:
        webhook_event = payload.get('webhookEvent', '')
        issue = payload.get('issue', {})
        changelog = payload.get('changelog', {})
        
        issue_key = issue.get('key', 'unknown')
        logger.info(f"Jira webhook: {webhook_event} for {issue_key}")
        
        # Check if this is our epic or a child issue
        if not issue_key.startswith('DOM2-'):
            logger.info(f"Ignoring issue {issue_key} (not DOM2 project)")
            return {'status': 'ignored'}
        
        # Process based on event type
        if webhook_event == 'jira:issue_updated':
            return handle_issue_updated(issue, changelog)
        elif webhook_event == 'jira:issue_created':
            return handle_issue_created(issue)
        else:
            logger.info(f"Ignoring event type: {webhook_event}")
            return {'status': 'ignored'}
            
    except Exception as e:
        logger.error(f"Error handling Jira webhook: {e}")
        return {'error': str(e)}


def handle_issue_updated(issue, changelog):
    """Handle issue updated event."""
    try:
        issue_key = issue.get('key', '')
        items = changelog.get('items', [])
        
        changes = []
        for item in items:
            field = item.get('field', '')
            old_value = item.get('fromString', '')
            new_value = item.get('toString', '')
            
            changes.append({
                'field': field,
                'old': old_value,
                'new': new_value
            })
        
        logger.info(f"Issue {issue_key} updated: {len(changes)} field(s) changed")
        
        # TODO: Trigger Jira sync
        # - Import sync-agent
        # - Run Jira sync for this issue
        # - Update tracks.md, child-issues.md, track directories
        # - Update changelog
        
        return {
            'status': 'processed',
            'issue': issue_key,
            'changes': len(changes)
        }
        
    except Exception as e:
        logger.error(f"Error handling issue update: {e}")
        return {'error': str(e)}


def handle_issue_created(issue):
    """Handle issue created event."""
    try:
        issue_key = issue.get('key', '')
        logger.info(f"New issue created: {issue_key}")
        
        # TODO: Trigger Jira sync
        # - Add to tracks.md
        # - Add to child-issues.md
        # - Create track directory if needed
        
        return {
            'status': 'processed',
            'issue': issue_key,
            'action': 'created'
        }
        
    except Exception as e:
        logger.error(f"Error handling issue creation: {e}")
        return {'error': str(e)}
