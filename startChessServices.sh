#!/bin/bash

projectPath=$(pwd)
# Check if the virtual environment already exists
if [ ! -d "$projectPath/venv" ]; then
    # Create the virtual environment
    python3 -m venv "$projectPath/venv"
fi

# Activate the virtual environment
source "$projectPath/venv/bin/activate"

# Check if the necessary Python packages are installed
pip install -r "$projectPath/requirements.txt"

mkdir -p $projectPath/Logs
cd $projectPath/Logs
touch ChessFetcher.log
touch ChessAnalyzer.log
cd $projectPath
# Get input from the user to create .env file
python3 setUpEnv.py
# Run the initialization command
python3 ChessDBUpdatingService.py init >> $projectPath/Logs/ChessFetcher.log 2>&1
python3 ChessAnalyzingService.py >> $projectPath/Logs/ChessAnalyzer.log 2>&1 &

PYTHON_PATH=$(which python3)

# Combine both cron jobs with output redirection to logs
(crontab -l 2>/dev/null; \
echo "0 23 * * * $PYTHON_PATH $projectPath/ChessDBUpdatingService.py std >> $projectPath/Logs/ChessFetcher.log 2>&1"; \
echo "0 0 * * * $PYTHON_PATH $projectPath/ChessAnalyzingService.py >> $projectPath/Logs/ChessAnalyzer.log 2>&1") | crontab -
