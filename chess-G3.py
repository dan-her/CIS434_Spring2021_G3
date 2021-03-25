# !usr/bin/python
import chess
import tkinter as tk
import sys

def startup():
    # initialize the board
    board = chess.Board()
    print("Whee!")
    while True:
        move = input()
        if (move == "exit" or move == "quit" or move == "q"):
            sys.exit()
        
        if (chess.Move.from_uci(move) in board.legal_moves):
            x = chess.Move.from_uci(move)
            board.push(x)
        else:
            print("error: bad move")
        
        if (board.is_checkmate()):
            print("g'over")
            sys.exit()
        
        print(board)
        

startup();
