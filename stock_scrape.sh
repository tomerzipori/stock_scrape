#!/bin/bash

# Set the path to the Python script
PYTHON_SCRIPT="/app/scrape.py"

# Set the Python interpreter
PYTHON_INTERPRETER="python"

# Log file location
LOG_FILE="/app/process_log.txt"

# Path to the Git repo
REPO_DIR="/app"

# File to commit
CSV_FILE="/app/prices.csv"

# Git branch
BRANCH="master"

# Start the log file with a timestamp (append to the file)
echo "Process started at $(date)" >> "$LOG_FILE"

# Run Python script and log output (append to the log file)
echo "Running Python script..." >> "$LOG_FILE"

$PYTHON_INTERPRETER $PYTHON_SCRIPT >> "$LOG_FILE" 2>&1

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Scraping completed successfully" >> "$LOG_FILE"
else
    echo "Scraping script encountered an error. Check the details below:" >> "$LOG_FILE"
fi

# End the log file with a timestamp (append to the file)
echo "Process ended at $(date)" >> "$LOG_FILE"

# Navigate to the repository
cd "$REPO_DIR" || exit

# Add the CSV file to the staging area
git add "$CSV_FILE" >> "$LOG_FILE" 2>&1

# Add the log file to the staging area
git add "$LOG_FILE" >> "$LOG_FILE" 2>&1

# Commit changes
git commit -m "Updated prices.csv and process log" >> "$LOG_FILE" 2>&1

# Push changes to GitHub
git push origin "$BRANCH" >> "$LOG_FILE" 2>&1
