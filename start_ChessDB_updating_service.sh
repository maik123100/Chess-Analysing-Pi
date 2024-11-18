#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Check if the necessary Python packages are installed
#pip3 install --break-system-packages -r requirements.txt

# Run the initialization command
python3 ChessDB_updating_service.py init
python3 Chess_analyzing_service.py >> ~/Projects/Logs/ChessAnalyzer.log 2>&1 &

# Get the full path of python3
PYTHON_PATH=$(which python3)

# Ensure the Logs directory exists
mkdir -p ~/Projects/Logs

# Combine both cron jobs with output redirection to logs
(crontab -l 2>/dev/null; \
echo "0 23 * * * $PYTHON_PATH ~/Projects/Chess-Analysing-Pi/ChessDB_updating_service.py std >> ~/Projects/Logs/ChessFetcher.log 2>&1"; \
echo "0 0 * * * $PYTHON_PATH ~/Projects/Chess-Analysing-Pi/Chess_analyzing_service.py >> ~/Projects/Logs/ChessAnalyzer.log 2>&1") | crontab -
