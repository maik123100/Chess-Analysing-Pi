import chess
import chess.engine

stockfishPath="/home/Maik/Projects/Stockfish/src/stockfish"
testFen="6k1/4q1p1/2p3Qp/2p5/2Pb2PP/1P2r3/6K1/5R2 w - - 3 40"


def get_Best_line(fen,threads,depth):
    engine=chess.engine.SimpleEngine.popen_uci(stockfishPath)
    engine.configure({"Threads": threads})
    board=chess.Board(fen)
    info=engine.analyse(board,chess.engine.Limit(depth=depth))
    return info["pv"]

if __name__=="__main__":
    print(f" Best line for position {testFen} is:{get_Best_line(testFen,4,21)}")