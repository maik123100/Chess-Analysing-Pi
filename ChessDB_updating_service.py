import subprocess
import pprint
import json
from datetime import datetime
import time
import mysql.connector
import os


def get_today_games_by_username(username):
    # Construct the URL for fetching today's games for the given username
    base_url = f"https://api.chess.com/pub/player/{username}/games/{datetime.now().strftime('%Y/%m')}"

    # Run curl command to make the HTTP request
    command = ["curl", base_url]
    try:
        # Execute the curl command and capture the output
        response = subprocess.run(command, capture_output=True, text=True, check=True)
        json_data = json.loads(response.stdout)
        return filterTodayGames(json_data['games'])
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
    # Split the PGN string into a list of moves and the result
    moves_and_result = pgn.split()
    moves_and_result = [move for move in moves_and_result if "..." not in move]
    moves = moves_and_result[:-1]
    win = moves_and_result[-1]

    # Split the moves into tuples of (move number, white move, black move)
    moves = [(moves[i], moves[i+1], moves[i+2]) for i in range(0, len(moves), 3)]

    # Create the object
    pgn_object = {
        "moves": moves,
        "win": win
    }

    return pgn_object

def trimJSONData(json_game):
    start_index = json_game["pgn"].index("1. ")
    better_pgn = json_game["pgn"][start_index:]
    better_pgn = removeTimestamps(better_pgn)
    better_pgn=pgn_in_object_Format(better_pgn)
    #better_pgn = pgn_in_object_Format(better_pgn)
    trimmed = {
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
    
def get_JSONgames_for_db_by_username(username):
    games = get_today_games_by_username(username)
    JSONgames_Array = []
    for game in games:
        JSONgames_Array.append(trimJSONData(game))
    return JSONgames_Array

def push_games_to_db(games):
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    db.close()
    pass


if __name__ == "__main__":
    games= get_JSONgames_for_db_by_username(os.getenv("CHESS_USERNAME"))
    pprint.pprint(games)