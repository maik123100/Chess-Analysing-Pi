FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y cron
RUN pip install --no-cache-dir -r requirements.txt
RUN (crontab -l ; echo "0 23 * * * python /app/ChessDB_updating_service.py >> /var/log/cron.log 2>&1") | crontab
CMD cron && tail -f /var/log/cron.log