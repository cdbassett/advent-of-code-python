#!/bin/bash

# Configuration files
TRACK_FILE=".success_log.txt"
TIMEOUT_LOG="timeouts.txt"
ERROR_LOG="errors.txt"

# Ensure tracking files exist
touch "$TRACK_FILE"
touch "$TIMEOUT_LOG"

# Find and loop through all Python scripts
find . -name "*.py" | while read -r f; do
    
    # Skip scripts that succeeded in a previous run
    if grep -qxF "$f" "$TRACK_FILE"; then
        continue
    fi

    # Skip scripts that timed out in a previous run
    if grep -qxF "$f" "$TIMEOUT_LOG"; then
        continue
    fi

    echo "Starting $f..."
    
    # Run the script with a 30-second timeout
    # Redirect stdout to null, capture stderr in a temporary file
    timeout 30 python3 "$f" >/dev/null 2>".tmp_err"
    EXIT_CODE=$?

    # Handle the execution results
    if [ $EXIT_CODE -eq 124 ]; then
        echo "⏰ Timeout in $f"
        echo "$f" >> "$TIMEOUT_LOG"
    elif [ $EXIT_CODE -eq 0 ]; then
        echo "$f" >> "$TRACK_FILE"
    else
        echo "❌ Exception in $f"
        {
            echo "=== Error in $f ==="
            cat ".tmp_err"
            echo -e "\n"
        } >> "$ERROR_LOG"
    fi

    # Clean up temporary error file
    rm -f ".tmp_err"
done
