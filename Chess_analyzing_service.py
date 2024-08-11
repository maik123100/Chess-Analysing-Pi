import chess
import chess.engine
import re
import psycopg2
import os
import sys
import pprint
from dotenv import load_dotenv
from typing import List, Tuple

stockfishPath="/home/Maik/Projects/Stockfish/src/stockfish"
testFen="6k1/4q1p1/2p3Qp/2p5/2Pb2PP/1P2r3/6K1/5R2 w - - 3 40"

def get_Best_line(fen:str,threads:int,depth:int)->Tuple[List[chess.Move],chess.engine.PovScore]:
    """
    Computes the best line of moves for a given FEN position
    Args:
        fen (str): FEN string of the position
        threads (int): Number of threads to use max 4
        depth (int): Depth of the search
    Returns:
        tuple: Tuple containing:
            - list: List of moves in the best line
            - str: Score of the best line
    """
    engine=chess.engine.SimpleEngine.popen_uci(stockfishPath)
    engine.configure({"Threads": threads})
    board=chess.Board(fen)
    info=engine.analyse(board,chess.engine.Limit(depth=depth))
    engine.quit()
    return (info["pv"],info["score"])

def convert_to_pgn(board: chess.Board, moves: List[chess.Move]) -> List[str]:
    """
    Converts a list of moves from UCI format to PGN (SAN) notation.

    Args:
        board (chess.Board): The starting board position.
        moves (List[chess.Move]): List of moves in UCI format.

    Returns:
        List[str]: List of moves in PGN (SAN) notation.
    """
    pgn_moves = []
    for move in moves:
        pgn_moves.append(board.san(move))
        board.push(move)
    return pgn_moves

def getGamesFromDB()->List[str]:
    """
    Fetches the games from the database
    Returns:
        list: List of games
    """
    load_dotenv()
    print("Fetching games from the database...")
    db = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )
    cursor=db.cursor()

    fetch_games_query = """
    SELECT uuid, white_username, white_rating, black_username, black_rating, time_control, pgn, win 
    FROM games
    """
    cursor.execute(fetch_games_query)
    games = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    db.close()

    # Convert the fetched data into a list of dictionaries
    games_list = []
    for game in games:
        game_dict = {
            "uuid": game[0],
            "white_username": game[1],
            "white_rating": game[2],
            "black_username": game[3],
            "black_rating": game[4],
            "time_control": game[5],
            "pgn": game[6],
            "win": game[7]
        }
        games_list.append(game_dict)

    return games_list

def getFensFromMoveList(moves:List[chess.Move])->List[str]:
    """
    Gets the FEN string of the position after a list of moves
    Args:
        moves (list): List of moves
    Returns:
        str: FEN string
    """
    fens=[]
    board=chess.Board()
    for move in moves:
        print(f"Creating FEN for move: {move}")
        board.push_san(move)
        fens.append(board.fen())
    return fens

if __name__=="__main__":
    print("Games in the database:")
    games=getGamesFromDB()
    for game in games:
        print("Game:",game["uuid"])
        moves = re.findall(r'\b(?:[a-h][1-8](?:=[NBRQ])?|O-O(?:-O)?|[NBRQK]?[a-h]?[1-8]?[x-]?[a-h][1-8](?:=[NBRQ])?[+#]?)\b', game["pgn"])
        try:
            fens = getFensFromMoveList(moves)
            for fen in fens:
                print("FEN:")
                pprint.pprint(fens)
                print(f"Best line: {get_Best_line(fen,4,21)}")
        except chess.IllegalMoveError:
            print("Illegal move error occured in game")
            pprint.pprint(game)
            print("If this happens create a new issue on github and attach everything from Illegal move error occured in game to this line")
            sys.exit(1)
