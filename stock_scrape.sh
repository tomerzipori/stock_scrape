#!/bin/bash

# Set the path to the python script
PYTHON_SCRIPT="C:\Users\Tomer\Documents\GitHub\stock_scrape\scrape.py"

# Set the Python interperter (van change to `python` if `python3` not available)
PYTHON_INTERPRETER="C:\Users\Tomer\Documents\GitHub\stock_scrape\.venv\Scripts\python.exe"

# Log file location
LOG_FILE="C:\Users\Tomer\Documents\GitHub\stock_scrape\scrape_errors.log"

# Path to the Git repo
REPO_DIR="C:\Users\Tomer\Documents\GitHub\stock_scrape"

# File to commit
CSV_FILE="prices.csv"

# Git branch
BRANCH="master"

# Print a start message
echo "Started scraping..."

# Run Python script
$PYTHON_INTERPRETER $PYTHON_SCRIPT

# Check if ran successfully
if [ $? -eq 0 ]; then
	echo "Scraping completed successfully"

	#  Navigate to the repository
	cd "$REP_DIR" || exit

	# Add the csv file to the staging area
	git add "$CSV_FILE"

	# Commit changes
	git commit -m "Updated prices.csv"

	# Push changes to Github
	git push origin "$BRANCH"

	echo "CSV file committed and pushed to Github successfully"
else
	echo "Scraping script encountered an error. Check the log file ($LOG_FILE) for details."
fi

