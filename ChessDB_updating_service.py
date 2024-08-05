import subprocess
import pprint
import json
from datetime import datetime, timedelta
import time
import psycopg2
import os
import sys
from dotenv import load_dotenv

def get_today_games_by_username(username):
    base_url = f"https://api.chess.com/pub/player/{username}/games/{datetime.now().strftime('%Y/%m')}"
    command = ["curl", base_url]
    try:
        response = subprocess.run(command, capture_output=True, text=True, check=True)
        json_data = json.loads(response.stdout)
        return filterTodayGames(json_data['games'])
    except subprocess.CalledProcessError as e:
        print(f"Error fetching data for {username}: {e}")
        return None

def get_last_month_games_by_username(username):
    base_url = f"https://api.chess.com/pub/player/{username}/games/{datetime.now().strftime('%Y/%m')}"
    base_url_last_month = f"https://api.chess.com/pub/player/{username}/games/{(datetime.now() - timedelta(days=30)).strftime('%Y/%m')}"
    command = ["curl", base_url]
    try:
        response = subprocess.run(command, capture_output=True, text=True, check=True)
        response_last_month = subprocess.run(["curl", base_url_last_month], capture_output=True, text=True, check=True)
        json_data = json.loads(response.stdout)
        json_data_last_month = json.loads(response_last_month.stdout)
        for game in json_data_last_month['games']:
            json_data['games'].append(game)
        return json_data['games']
    except subprocess.CalledProcessError as e:
        print(f"Error fetching data for {username}: {e}")
        return None

def filterTodayGames(games):
    today = f"[Event \"Live Chess\"]\n[Site \"Chess.com\"]\n[Date \"{datetime.now().strftime('%Y.%m.%d')}\"]"
    today_games = []
    for game in games:
        if game["pgn"].startswith(today):
            today_games.append(game)
    return today_games

def removeTimestamps(pgn):
    while '{' in pgn:
        start = pgn.find('{')
        end = pgn.find('}')
        pgn = pgn[:start] + pgn[end+1:]
    return pgn

def pgn_in_object_Format(pgn):
    moves_and_result = pgn.split()
    moves_and_result = [move for move in moves_and_result if "..." not in move]
    moves = moves_and_result[:-1]
    win = moves_and_result[-1]
    moves = [(moves[i], moves[i+1], moves[i+2] if i+2 < len(moves) else "None") for i in range(0, len(moves), 3)]
    pgn_object = {
        "moves": moves,
        "win": win
    }
    return pgn_object

def trimJSONData(json_game):
    start_index = json_game["pgn"].index("1. ")
    better_pgn = json_game["pgn"][start_index:]
    better_pgn = removeTimestamps(better_pgn)
    better_pgn = pgn_in_object_Format(better_pgn)
    trimmed = {
        "uuid": json_game["uuid"],
        "white": {
            "username": json_game["white"]["username"],
            "rating": json_game["white"]["rating"]
        },
        "black": {
            "username": json_game["black"]["username"],
            "rating": json_game["black"]["rating"]
        },
        "time_control": json_game["time_control"],
        "structured_pgn": better_pgn
    }
    return trimmed

def get_JSON_Month_games_for_db_by_username(username):
    print(f"Fetching games for {username}")
    games = get_last_month_games_by_username(username)
    JSONgames_Array = []
    for game in games:
        JSONgames_Array.append(trimJSONData(game))
    return JSONgames_Array

def get_JSONgames_for_db_by_username(username):
    print(f"Fetching games for {username}")
    games = get_today_games_by_username(username)
    JSONgames_Array = []
    for game in games:
        JSONgames_Array.append(trimJSONData(game))
    return JSONgames_Array

def push_games_to_db(games):
    print("Pushing games to the database...")
    db = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

    cursor = db.cursor()

    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS games (
        uuid VARCHAR(255) PRIMARY KEY,
        white_username VARCHAR(255),
        white_rating INTEGER,
        black_username VARCHAR(255),
        black_rating INTEGER,
        time_control VARCHAR(50),
        pgn TEXT,
        win VARCHAR(10)
    )
    """
    cursor.execute(create_table_query)
    db.commit()

    for game in games:
        sql = """INSERT INTO games(uuid, white_username, white_rating, black_username, black_rating, time_control, pgn, win)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (game['uuid'], game['white']['username'], game['white']['rating'], game['black']['username'], game['black']['rating'], game['time_control'], ''.join(str(move) for move in game['structured_pgn']['moves']), game['structured_pgn']['win'])
        print("SQL query prepared")
        try:
            cursor.execute(sql, values)
            print("Game inserted")
            db.commit()
            print("Game committed")
        except Exception as e:
            print(f"Error inserting game: {game}")
            print(f"Error: {e}")
            db.rollback()

    cursor.close()
    db.close()

if __name__ == "__main__":
    load_dotenv()
    print(f"ENV_Test: {os.getenv('ENV_Test')}")
    if os.getenv("ENV_Test") == "test":
        pprint.pprint(get_last_month_games_by_username(os.getenv("CHESS_USERNAME")))
    elif os.getenv("ENV_Test") == "prod":
        if len(sys.argv) != 2:
            print("Please provide one argument: 'init' for initialization or 'std' for standard execution")
        else:
            arg = sys.argv[1]
            games = None
            if arg == 'init':
                print("Initializing the database with the last month worth of games...")
                games=get_JSON_Month_games_for_db_by_username(os.getenv("CHESS_USERNAME"))
                pprint.pprint(games)
            elif arg == 'std':
                print("Standard execution...")
                games = get_JSONgames_for_db_by_username(os.getenv("CHESS_USERNAME"))
            else:
                print("Invalid argument. Please provide 'init' for initialization or 'std' for standard execution")
                sys.exit(1)
            push_games_to_db(games)
    else:
        print("Invalid value for ENV_Test")
        raise Exception("ENV_Test must be set to either 'test' or 'prod'")