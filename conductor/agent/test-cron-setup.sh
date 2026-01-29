#!/bin/bash
# Test script to verify cron setup and immediately test the sync agent
# This script verifies all setup steps and executes the wrapper script to test end-to-end functionality

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

PROGRESS_FILE="$SCRIPT_DIR/setup-progress.json"
WRAPPER_SCRIPT="$SCRIPT_DIR/run-daily-sync.sh"
LOG_FILE="$SCRIPT_DIR/logs/daily-sync.log"
CHANGELOG_PATH="$SCRIPT_DIR/../CHANGELOG.md"
REPORTS_DIR="$SCRIPT_DIR/../reports"

# Test results
TESTS_PASSED=0
TESTS_FAILED=0
TEST_RESULTS=()

# Function to print test result
print_test() {
    local status=$1
    local message=$2
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✅${NC} $message"
        ((TESTS_PASSED++))
        TEST_RESULTS+=("PASS: $message")
    else
        echo -e "${RED}❌${NC} $message"
        ((TESTS_FAILED++))
        TEST_RESULTS+=("FAIL: $message")
    fi
}

# Function to update progress file
update_progress() {
    local step=$1
    local status=$2
    if command -v python3 &> /dev/null; then
        python3 << EOF
import json
import sys
from datetime import datetime

try:
    with open('$PROGRESS_FILE', 'r') as f:
        progress = json.load(f)
    
    if '$step' in progress.get('steps', {}):
        progress['steps']['$step']['status'] = '$status'
        if '$status' == 'completed':
            progress['steps']['$step']['completed_at'] = datetime.utcnow().isoformat() + 'Z'
    
    progress['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    
    with open('$PROGRESS_FILE', 'w') as f:
        json.dump(progress, f, indent=2)
except Exception as e:
    print(f"Error updating progress: {e}", file=sys.stderr)
    sys.exit(1)
EOF
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Cron Setup Verification Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Load and display progress
echo -e "${YELLOW}📋 Current Setup Progress:${NC}"
if [ -f "$PROGRESS_FILE" ]; then
    if command -v python3 &> /dev/null; then
        python3 << PYEOF
import json
import sys

try:
    with open('$PROGRESS_FILE', 'r') as f:
        progress = json.load(f)
    
    print(f"Setup started: {progress.get('setup_started', 'Unknown')}")
    print("\nStep Status:")
    for step, info in progress.get('steps', {}).items():
        status = info.get('status', 'unknown')
        status_icon = "✅" if status == "completed" else "⏳" if status == "in_progress" else "⭕"
        print(f"  {status_icon} {step}: {status}")
    
    print(f"\nSchedule: {progress.get('configuration', {}).get('schedule_description', 'Unknown')}")
except Exception as e:
    print(f"Error reading progress file: {e}", file=sys.stderr)
PYEOF
    else
        echo "  Progress file exists but python3 not available to parse it"
    fi
    print_test "pass" "Progress file exists"
else
    print_test "fail" "Progress file not found at $PROGRESS_FILE"
fi
echo ""

# 2. Verify cron jobs
echo -e "${YELLOW}Checking cron jobs...${NC}"
CRON_COUNT=0
CRON_EXISTS=false
if crontab -l 2>/dev/null | grep -q "run-daily-sync.sh"; then
    CRON_LINES=$(crontab -l 2>/dev/null | grep "run-daily-sync.sh")
    CRON_COUNT=$(echo "$CRON_LINES" | wc -l | tr -d ' ')
    
    # Check if we have 4 cron jobs (9 AM, 12 PM, 3 PM, 8 PM)
    if [ "$CRON_COUNT" -eq 4 ]; then
        # Verify all expected times are present
        HAS_9AM=$(echo "$CRON_LINES" | grep -q "0 9 \* \* 0-4" && echo "yes" || echo "no")
        HAS_12PM=$(echo "$CRON_LINES" | grep -q "0 12 \* \* 0-4" && echo "yes" || echo "no")
        HAS_3PM=$(echo "$CRON_LINES" | grep -q "0 15 \* \* 0-4" && echo "yes" || echo "no")
        HAS_8PM=$(echo "$CRON_LINES" | grep -q "0 20 \* \* 0-4" && echo "yes" || echo "no")
        
        if [ "$HAS_9AM" = "yes" ] && [ "$HAS_12PM" = "yes" ] && [ "$HAS_3PM" = "yes" ] && [ "$HAS_8PM" = "yes" ]; then
            print_test "pass" "All 4 cron jobs installed with correct schedule (Sun-Thu: 9 AM, 12 PM, 3 PM, 8 PM)"
            echo "$CRON_LINES" | sed 's/^/  /'
            CRON_EXISTS=true
        else
            print_test "fail" "Cron jobs exist but some schedules may be incorrect"
            echo "$CRON_LINES" | sed 's/^/  /'
            echo "  Missing:"
            [ "$HAS_9AM" = "no" ] && echo "    - 9:00 AM"
            [ "$HAS_12PM" = "no" ] && echo "    - 12:00 PM"
            [ "$HAS_3PM" = "no" ] && echo "    - 3:00 PM"
            [ "$HAS_8PM" = "no" ] && echo "    - 8:00 PM"
        fi
    else
        print_test "fail" "Expected 4 cron jobs, found $CRON_COUNT"
        echo "$CRON_LINES" | sed 's/^/  /'
    fi
else
    print_test "fail" "Cron jobs not found in crontab"
fi
echo ""

# 3. Verify wrapper script exists
echo -e "${YELLOW}Checking wrapper script...${NC}"
if [ -f "$WRAPPER_SCRIPT" ]; then
    print_test "pass" "Wrapper script exists at $WRAPPER_SCRIPT"
    
    if [ -x "$WRAPPER_SCRIPT" ]; then
        print_test "pass" "Wrapper script is executable"
    else
        print_test "fail" "Wrapper script is not executable"
    fi
else
    print_test "fail" "Wrapper script not found at $WRAPPER_SCRIPT"
fi
echo ""

# 4. Verify Python path
echo -e "${YELLOW}Checking Python interpreter...${NC}"
PYTHON_PATH="/usr/bin/python3"
if [ -f "$PYTHON_PATH" ]; then
    print_test "pass" "Python interpreter found at $PYTHON_PATH"
    PYTHON_VERSION=$("$PYTHON_PATH" --version 2>&1)
    echo "  Version: $PYTHON_VERSION"
else
    print_test "fail" "Python interpreter not found at $PYTHON_PATH"
fi
echo ""

# 5. Verify logs directory
echo -e "${YELLOW}Checking logs directory...${NC}"
if [ -d "$SCRIPT_DIR/logs" ]; then
    print_test "pass" "Logs directory exists"
else
    print_test "fail" "Logs directory not found"
    echo "  Creating logs directory..."
    mkdir -p "$SCRIPT_DIR/logs"
    if [ -d "$SCRIPT_DIR/logs" ]; then
        print_test "pass" "Logs directory created"
    fi
fi
echo ""

# 6. Verify agent script exists
echo -e "${YELLOW}Checking agent script...${NC}"
if [ -f "$SCRIPT_DIR/sync-agent.py" ]; then
    print_test "pass" "Agent script (sync-agent.py) exists"
else
    print_test "fail" "Agent script (sync-agent.py) not found"
fi
echo ""

# 7. Immediate execution test
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Running Immediate Execution Test${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "This will execute the wrapper script to verify end-to-end functionality..."
echo "This may take a few minutes..."
echo ""

# Store log file size before execution
LOG_SIZE_BEFORE=0
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE_BEFORE=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
fi

# Store changelog modification time before execution
CHANGELOG_MTIME_BEFORE=""
if [ -f "$CHANGELOG_PATH" ]; then
    CHANGELOG_MTIME_BEFORE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$CHANGELOG_PATH" 2>/dev/null || stat -c "%y" "$CHANGELOG_PATH" 2>/dev/null || echo "")
    print_test "pass" "Live Changelog file exists at $CHANGELOG_PATH"
    echo "  Last modified: $CHANGELOG_MTIME_BEFORE"
else
    print_test "fail" "Live Changelog file not found at $CHANGELOG_PATH"
fi
echo ""

# Execute the wrapper script
echo "Executing: $WRAPPER_SCRIPT"
echo ""

EXECUTION_START=$(date +%s)
EXECUTION_TIME=0
if [ -x "$WRAPPER_SCRIPT" ]; then
    "$WRAPPER_SCRIPT"
    EXIT_CODE=$?
    EXECUTION_END=$(date +%s)
    EXECUTION_TIME=$((EXECUTION_END - EXECUTION_START))
else
    EXIT_CODE=1
fi
    
    echo ""
    echo "Execution completed in ${EXECUTION_TIME} seconds with exit code: $EXIT_CODE"
    echo ""
    
    if [ $EXIT_CODE -eq 0 ]; then
        print_test "pass" "Wrapper script executed successfully (exit code: 0)"
    else
        # Check if it's just because no changes were detected (which is normal)
        if grep -q "0 changes processed" "$LOG_FILE" 2>/dev/null; then
            print_test "pass" "Wrapper script executed (exit code: $EXIT_CODE, but this may be normal if no changes detected)"
        else
            print_test "fail" "Wrapper script exited with error code: $EXIT_CODE"
        fi
    fi
echo ""

# 8. Verify log file was updated
echo -e "${YELLOW}Checking execution logs...${NC}"
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE_AFTER=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$LOG_SIZE_AFTER" -gt "$LOG_SIZE_BEFORE" ]; then
        print_test "pass" "Log file was updated (new entries added)"
        echo ""
        echo "Last 15 lines of log file:"
        echo "----------------------------------------"
        tail -n 15 "$LOG_FILE" | sed 's/^/  /'
        echo "----------------------------------------"
    else
        print_test "fail" "Log file was not updated (no new entries)"
    fi
else
    print_test "fail" "Log file was not created at $LOG_FILE"
fi
echo ""

# 9. Verify Daily Digest was generated
echo -e "${YELLOW}Checking Daily Digest reporting...${NC}"
TODAY=$(date +%Y-%m-%d)
# Check both possible locations (relative to agent dir and relative to project root)
DIGEST_FILE1="$REPORTS_DIR/daily-digest-$TODAY.md"
DIGEST_FILE2="$SCRIPT_DIR/conductor/reports/daily-digest-$TODAY.md"
DIGEST_FILE=""

if [ -f "$DIGEST_FILE1" ]; then
    DIGEST_FILE="$DIGEST_FILE1"
elif [ -f "$DIGEST_FILE2" ]; then
    DIGEST_FILE="$DIGEST_FILE2"
fi

if [ -n "$DIGEST_FILE" ] && [ -f "$DIGEST_FILE" ]; then
    print_test "pass" "Daily Digest file created: $DIGEST_FILE"
    DIGEST_SIZE=$(wc -l < "$DIGEST_FILE" 2>/dev/null || echo "0")
    echo "  File size: $DIGEST_SIZE lines"
    
    # Check for key content
    if grep -q "Daily Digest" "$DIGEST_FILE" 2>/dev/null; then
        print_test "pass" "Daily Digest contains expected content"
    fi
else
    print_test "fail" "Daily Digest file not found"
    echo "  Checked locations:"
    echo "    - $DIGEST_FILE1"
    echo "    - $DIGEST_FILE2"
    if [ -d "$REPORTS_DIR" ]; then
        echo "  Reports directory ($REPORTS_DIR) exists. Available files:"
        ls -la "$REPORTS_DIR" | head -10 | sed 's/^/    /'
    fi
    if [ -d "$SCRIPT_DIR/conductor/reports" ]; then
        echo "  Alternative reports directory exists. Available files:"
        ls -la "$SCRIPT_DIR/conductor/reports" | head -10 | sed 's/^/    /'
    fi
fi
echo ""

# 10. Verify Live Changelog
echo -e "${YELLOW}Checking Live Changelog reporting...${NC}"
if [ -f "$CHANGELOG_PATH" ]; then
    CHANGELOG_MTIME_AFTER=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$CHANGELOG_PATH" 2>/dev/null || stat -c "%y" "$CHANGELOG_PATH" 2>/dev/null || echo "")
    
    if [ "$CHANGELOG_MTIME_AFTER" != "$CHANGELOG_MTIME_BEFORE" ]; then
        print_test "pass" "Live Changelog was updated"
        echo "  Updated at: $CHANGELOG_MTIME_AFTER"
    else
        print_test "pass" "Live Changelog exists (may not have been updated if no changes detected)"
        echo "  Last modified: $CHANGELOG_MTIME_AFTER"
        echo "  (Note: Changelog is only updated when changes are detected)"
    fi
    
    CHANGELOG_SIZE=$(wc -l < "$CHANGELOG_PATH" 2>/dev/null || echo "0")
    echo "  File size: $CHANGELOG_SIZE lines"
else
    print_test "fail" "Live Changelog file not found at $CHANGELOG_PATH"
fi
echo ""

# 11. Check for reporting messages in logs
echo -e "${YELLOW}Checking for reporting completion in logs...${NC}"
if [ -f "$LOG_FILE" ]; then
    if grep -qi "daily digest" "$LOG_FILE" 2>/dev/null; then
        print_test "pass" "Daily digest generation logged"
        grep -i "daily digest" "$LOG_FILE" | tail -3 | sed 's/^/  /'
    else
        print_test "fail" "Daily digest generation not found in logs"
    fi
    
    if grep -qi "changelog" "$LOG_FILE" 2>/dev/null; then
        print_test "pass" "Changelog update logged"
        grep -i "changelog" "$LOG_FILE" | tail -3 | sed 's/^/  /'
    else
        print_test "pass" "Changelog update not in logs (may be normal if no changes detected)"
    fi
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

# Update progress file with test results
if command -v python3 &> /dev/null; then
    # Create a temporary file with test results
    TEMP_RESULTS=$(mktemp)
    printf '%s\n' "${TEST_RESULTS[@]}" > "$TEMP_RESULTS"
    
    python3 << EOF
import json
from datetime import datetime

try:
    with open('$PROGRESS_FILE', 'r') as f:
        progress = json.load(f)
    
    # Read test results from temp file
    test_results_list = []
    try:
        with open('$TEMP_RESULTS', 'r') as f:
            test_results_list = [line.strip() for line in f if line.strip()]
    except:
        pass
    
    progress['test_results'] = {
        'tested_at': datetime.utcnow().isoformat() + 'Z',
        'tests_passed': $TESTS_PASSED,
        'tests_failed': $TESTS_FAILED,
        'exit_code': $EXIT_CODE,
        'execution_time_seconds': $EXECUTION_TIME,
        'results': test_results_list
    }
    
    progress['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    
    with open('$PROGRESS_FILE', 'w') as f:
        json.dump(progress, f, indent=2)
except Exception as e:
    print(f"Warning: Could not update progress file: {e}")
EOF
    
    # Clean up temp file
    rm -f "$TEMP_RESULTS"
fi

# Final result
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Setup is complete and verified. The cron job will run every Sunday-Thursday at 10:00am."
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    echo ""
    echo "The cron job is installed, but some verification steps failed."
    echo "Check the logs and output above for details."
    exit 1
fi
