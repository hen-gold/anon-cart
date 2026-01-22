"""
GitHub Webhook Handler

Handles GitHub webhook events for code commit monitoring.
"""

import logging
import json
from flask import Flask, request

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/webhook/github', methods=['POST'])
def handle_github_webhook():
    """
    Handle GitHub webhook events.
    
    Expected events:
    - push: Code commits
    - pull_request: PR opened/merged/closed
    """
    try:
        event = request.headers.get('X-GitHub-Event')
        payload = request.json
        
        logger.info(f"Received GitHub webhook: {event}")
        
        if event == 'push':
            return handle_push_event(payload)
        elif event == 'pull_request':
            return handle_pull_request_event(payload)
        else:
            logger.info(f"Ignoring event type: {event}")
            return {'status': 'ignored'}, 200
            
    except Exception as e:
        logger.error(f"Error handling GitHub webhook: {e}")
        return {'error': str(e)}, 500


def handle_push_event(payload):
    """Handle push event (code commits)."""
    try:
        repository = payload.get('repository', {})
        commits = payload.get('commits', [])
        
        repo_name = repository.get('full_name', 'unknown')
        branch = payload.get('ref', '').replace('refs/heads/', '')
        
        logger.info(f"Push event: {len(commits)} commits to {repo_name} on {branch}")
        
        # TODO: Trigger code sync
        # - Import sync-agent
        # - Run code sync for this repository
        # - Update context files
        # - Update changelog
        
        return {'status': 'processed', 'commits': len(commits)}, 200
        
    except Exception as e:
        logger.error(f"Error handling push event: {e}")
        return {'error': str(e)}, 500


def handle_pull_request_event(payload):
    """Handle pull request event."""
    try:
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        
        logger.info(f"PR event: {action} for PR #{pr.get('number', 'unknown')}")
        
        # Only process merged PRs
        if action == 'closed' and pr.get('merged'):
            # TODO: Trigger code sync
            # - PR was merged, sync code changes
            # - Update context files
            
            return {'status': 'processed', 'merged': True}, 200
        
        return {'status': 'ignored', 'action': action}, 200
        
    except Exception as e:
        logger.error(f"Error handling PR event: {e}")
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
