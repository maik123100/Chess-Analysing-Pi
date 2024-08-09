import chess
import chess.engine

stockfishPath="/home/Maik/Projects/Stockfish/src/stockfish"
testFen=""


def get_Best_line(fen,threads,depth):
    engine=chess.engine.SimpleEngine.popen_uci(stockfishPath)
    engine.configure({"Threads": threads})
    board=chess.Board(fen)
    info=engine.analyse(board,chess.engine.Limit(depth=depth))
    return info["pv"]

if __name__=="__main__":
    print(f" Best line for position {testFen} is:{get_Best_line(testFen,4,21)}")