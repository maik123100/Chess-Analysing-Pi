import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
import subprocess
import json

def getDBConnection()->psycopg2.extensions.connection:
    load_dotenv()
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

