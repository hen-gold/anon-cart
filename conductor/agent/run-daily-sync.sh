#!/bin/bash
# Sync agent - runs every Sun-Thu at 9:00 AM, 12:00 PM, 3:00 PM, and 8:00 PM
# This script runs the context synchronization agent in scheduled mode

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Change to project root (two levels up from agent directory to get to anon-cart root)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

# Log file with timestamp (relative to agent directory)
LOG_FILE="$SCRIPT_DIR/logs/daily-sync.log"

# Ensure logs directory exists
mkdir -p "$SCRIPT_DIR/logs"

# Add timestamp to log
echo "=========================================" >> "$LOG_FILE"
echo "Daily sync started at $(date)" >> "$LOG_FILE"
echo "=========================================" >> "$LOG_FILE"

# Run the sync agent in scheduled mode
# This will:
# - Perform full sync across all sources (code, Jira, docs, Slack)
# - Update live changelog if changes detected
# - Generate daily digest (forced in scheduled mode)
/usr/bin/python3 "$SCRIPT_DIR/sync-agent.py" --mode scheduled >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# Log completion
if [ $EXIT_CODE -eq 0 ]; then
    echo "Daily sync completed successfully at $(date)" >> "$LOG_FILE"
else
    echo "Daily sync completed with errors (exit code: $EXIT_CODE) at $(date)" >> "$LOG_FILE"
fi

echo "=========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE
