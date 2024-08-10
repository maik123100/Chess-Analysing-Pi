import chess
import chess.engine
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

if __name__=="__main__":
    line,score=get_Best_line(testFen,4,21)
    board = chess.Board(testFen)
    pgn_line = convert_to_pgn(board, line)
    print(f"Best line for position (Score:{score}) {testFen} is:{line}\n In PGN notation: {pgn_line}")