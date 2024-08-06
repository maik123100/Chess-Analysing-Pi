import subprocess
from time import sleep
import psycopg2
import os
from dotenv import load_dotenv

stockfishPath='../Stockfish/src/stockfish'

def runStockfishOnFen(fen,depth,threads,path):
    process= subprocess.Popen([path],
                              stdin=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              text=True)
    sleep(0.1)
    process.stdin.write(f"uci\n")
    process.stdin.write(f"setoption name Threads value {threads}\n")
    process.stdin.write(f"position feb {fen}\n")
    process.stdin.write(f"go depth {depth}\n")
    process.stdin.write(f"quit\n")
    process.stdin.flush()
    output,error=process.communicate()
    print(f"Encountered error:{error}")
    return output

if __name__=="__main__":
    fen="2kr4/p7/bbp3pp/5p2/2P5/5P2/1P2QNNq/2R2K2 b - - 1 31"
    depth=21
    threads=4
    print(runStockfishOnFen(fen,depth,threads,stockfishPath))
