#!/bin/bash

# Navigate to the cloned GitHub repository
cd /app || exit

# Git configuration
git config --global user.name "tomerzipori"
git config --global user.email "tomerzip@post.bgu.ac.il"

# Set the path to the Python script
PYTHON_SCRIPT="/app/scrape.py"

# Set the Python interpreter
PYTHON_INTERPRETER="python"

# Log file location
LOG_FILE="/app/process_log.txt"

# File to commit
CSV_FILE="/app/prices.csv"

# Git branch
BRANCH="master"

# Start the log file with a timestamp
echo "Process started at $(date)" >> "$LOG_FILE"

# Run Python script and log output
echo "Running Python script..." >> "$LOG_FILE"
$PYTHON_INTERPRETER $PYTHON_SCRIPT >> "$LOG_FILE" 2>&1

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Scraping completed successfully" >> "$LOG_FILE"
else
    echo "Scraping script encountered an error. Check the details below:" >> "$LOG_FILE"
    exit 1
fi

# End the log file with a timestamp
echo "Process ended at $(date)" >> "$LOG_FILE"

# Pull latest changes from remote before pushing
git pull --rebase origin master >> "$LOG_FILE" 2>&1

# Commit and push changes to GitHub
git add "$CSV_FILE" "$LOG_FILE"
git commit -m "Updated prices.csv and process log"
git push origin "$BRANCH"
