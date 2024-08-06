from stockfish import Stockfish

sf=Stockfish(path="../Stockfish/src/stockfish",depth=21)

if sf.is_fen_valid("r4r1k/ppp3p1/5n1q/3P4/3Q1p1P/2NB2PN/PPP2P2/R4RK1 b - - 0 18"):
    sf.set_fen_position("r4r1k/ppp3p1/5n1q/3P4/3Q1p1P/2NB2PN/PPP2P2/R4RK1 b - - 0 18")
    print(sf.get_best_move())
