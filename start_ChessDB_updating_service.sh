#!/bin/bash

# Check if the necessary python packages are installed
pip install -r requirements.txt

# Run the initialization command
python3 ChessDB_updating_service.py init

# Create a cron job to run the standard execution at 11 PM daily
(crontab -l 2>/dev/null; echo "0 23 * * * python3 ~/Projects/Chess-Analysing-Pi/ChessDB_updating_service.py std") | crontab -