import subprocess
from time import sleep
import psycopg2
import os
from dotenv import load_dotenv

stockfishPath='../Stockfish/src/stockfish'

def runStockfishOnFen(fen, depth, threads, path):
    process = subprocess.Popen([path],
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               text=True)
    sleep(0.1)
    
    # Send commands to Stockfish and print them
    commands = [
        "uci\n",
        f"setoption name Threads value {threads}\n",
        f"position fen {fen}\n",
        f"go depth {depth}\n",
        "quit\n"
    ]
    
    for command in commands:
        print(f"Sending command: {command.strip()}")
        process.stdin.write(command)
        process.stdin.flush()
        sleep(0.5)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())   
    
    error = process.stderr.read()
    if error:
        print(f"Encountered error: {error.strip()}")
    
    return output

if __name__=="__main__":
    fen="2kr4/p7/bbp3pp/5p2/2P5/5P2/1P2QNNq/2R2K2 b - - 1 31"
    depth=21
    threads=4
    print(runStockfishOnFen(fen,depth,threads,stockfishPath))
