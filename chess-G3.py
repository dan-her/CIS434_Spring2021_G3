import tkinter as tk
from tkinter import *
import chess
from PIL import ImageTk, Image

# global variables
squaresCount = 0 # for gameBackend
initPos = '' # for gameBackend



class gameBackend():
class GameBackend():
    def __init__(self, board, gui):
    	self.gui = gui
    	self.start = None
    	self.destination = None
    	self.board = board

    def squareUp(self, event, square):
        global initPos
        global squaresCount
        if (squaresCount == 1):
            initPos += square # the total move for the board (i.e. "e2e4")
            squaresCount = 0
            print(initPos)
            if (chess.Move.from_uci(initPos) in self.board.legal_moves): # check if the move is legal
            	x = chess.Move.from_uci(initPos) # create the move
        if self.start:
            self.destination = square # the total move for the board (i.e. "e2e4")
            if self.destination == self.start:
            	return
            move = self.start.name + self.destination.name
            if (chess.Move.from_uci(move) in self.board.legal_moves): # check if the move is legal
            	x = chess.Move.from_uci(move) # create the move
            	self.board.push(x) # put the move on the board
            	tempPiece = self.gui.getSquare(initPos).piece
            	self.gui.getSquare(square).piece = Piece(self.gui, tempPiece.name, square)
            	self.gui.getSquare(initPos).piece = None
            	clickt(initPos)

            	self.destination.piece = Piece(self.gui, self.start.piece.name, square.name)
            	self.start.piece = None # Get rid of piece reference to remove from board
            	self.start = None 
            	self.gui.historyUI.addHistory(move)
            else:
                print("error: bad move")
            if (self.board.is_checkmate()):
                print("g'over")
            print(self.board)
        else:
            initPos = square
            squaresCount = 1
            self.start = square



class ChessBoardGUI():
	def __init__(self, root):
	def InitPieces(self):
		for c in Square.SquareLetters:
			Piece(self, 'pawn_w', c + str(2))
			Piece(self, 'pawn_b', c + str(7))
		Piece(self, 'rook_w', 'a1')
		Piece(self, 'knight_w', 'b1')
		Piece(self, 'bishop_w', 'c1')
		Piece(self, 'queen_w', 'd1')
		Piece(self, 'king_w', 'e1')
		Piece(self, 'bishop_w', 'f1')
		Piece(self, 'knight_w', 'g1')
		Piece(self, 'rook_w', 'h1')
		Piece(self, 'rook_b', 'a8')
		Piece(self, 'knight_b', 'b8')
		Piece(self, 'bishop_b', 'c8')
		Piece(self, 'queen_b', 'd8')
		Piece(self, 'king_b', 'e8')
		Piece(self, 'bishop_b', 'f8')
		Piece(self, 'knight_b', 'g8')
		Piece(self, 'rook_b', 'h8')

	def __init__(self, root, historyUI):
		self.historyUI = historyUI
		self.root = root
		self.squares = [[Square(self, x, y) for x in range(8)] for y in range(8)]
		self.InitPieces()

	# Convert AN name of square into array indices and returns square
	# Get square from it's name
	def getSquare(self, squareName):
		colNum = Square.SquareLetters.index(squareName[0])
		rowNum = 8 - (int(squareName[1]))
@@ -56,18 +67,15 @@ class Square():
	SquareLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	def __init__(self, chessboard, x, y):
		self.name = Square.getSquareName(x, y)
		self.name = Square.SquareLetters[x] + str(8 - y)
		bgcolor = 'gray13'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
		self.piece = None
		self.chessboard = chessboard
		self.canvas = tk.Canvas(chessboard.root, bg = bgcolor, width=64, height=64, highlightthickness=0)  # Canvas with no border to represent each square
		self.canvas.grid(row = y, column = x) # Align to tkinter grid
		self.canvas.bind('<Button-1>', lambda a: backendBoard.squareUp(self.chessboard, self.name)) # Send name of square to the fcn that controls the board 
	def getSquareName(x, y):
		col = Square.SquareLetters[x]
		return col + str(8 - y)
		self.canvas.bind('<Button-1>', lambda a: backendBoard.squareUp(self.chessboard, self)) # Send name of square to the fcn that controls the board 

	# Get grid x/y coords from a square
	def getCoords(self):
		colNum = Square.SquareLetters.index(self.name[0])
		rowNum = 8 - (int(self.name[1]))
		return colNum, rowNum
class Piece():
	def __init__(self, chessboard, pieceName, squareName):
		self.name = pieceName
		path = "assets//"+pieceName + '.png'
		image = Image.open(path)
		image.thumbnail((48, 48)) # Resize the piece to fit (can also use image.resize I believe)
		image.thumbnail((48, 48)) 
		self.imgInternal = ImageTk.PhotoImage(image)
		chessboard.getSquare(squareName).canvas.create_image(32,32,image=self.imgInternal)
		chessboard.getSquare(squareName).piece = self


class MoveHistory():
	def __init__(self, root):
		historyFrame = tk.LabelFrame(root, text="history frame", padx = 5, pady = 5) 
		historyFrame.grid(row = 0, column = 1, padx=10, pady=10) 
		scrollbar = tk.Scrollbar(historyFrame) 
		scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
		self.listbox = tk.Listbox(historyFrame, yscrollcommand = scrollbar.set)
		self.listbox.pack(side = tk.LEFT, fill = tk.BOTH)
		self.history = []

	def addHistory(self, item):
		self.listbox.insert(tk.END, item)
		self.history.append(item)

def InitWindow():
	root = tk.Tk()
	root.geometry('768x640')
	root.title('Chess')
	root.configure(background='grey7')
	root.bind('<Escape>', lambda e: root.destroy())
	return root

def clickt(item): # authored by curtis gach
    mylist.insert(END, item) # authored by curtis gach

if __name__ == '__main__':
	root = InitWindow()
	boardFrame = Frame(root, padx='5', pady='5') # authored by curtis gach
	boardFrame.grid(row = 0, column = 0, padx=10, pady=10) # authored by curtis gach
	chessboard = ChessBoardGUI(boardFrame)
	backendBoard = gameBackend(chess.Board(), chessboard) # init backend board

	historyFrame = LabelFrame(root, text="history frame", padx = 5, pady = 5) # authored by curtis gach
	historyFrame.grid(row = 0, column = 1, padx=10, pady=10) # authored by curtis gach
	scrollbar = Scrollbar(historyFrame) # authored by curtis gach
	scrollbar.pack(side = RIGHT, fill = Y) # authored by curtis gach
	mylist = Listbox(historyFrame, yscrollcommand = scrollbar.set) # authored by curtis gach
	mylist.pack(side = LEFT, fill = BOTH) # authored by curtis gach


	for c in Square.SquareLetters:
		Piece(chessboard, 'pawn_w', c + str(2))
		Piece(chessboard, 'pawn_b', c + str(7))

	Piece(chessboard, 'rook_w', 'a1')
	Piece(chessboard, 'knight_w', 'b1')
	Piece(chessboard, 'bishop_w', 'c1')
	Piece(chessboard, 'queen_w', 'd1')
	Piece(chessboard, 'king_w', 'e1')
	Piece(chessboard, 'bishop_w', 'f1')
	Piece(chessboard, 'knight_w', 'g1')
	Piece(chessboard, 'rook_w', 'h1')
	boardFrame = tk.Frame(root, padx='5', pady='5') 
	boardFrame.grid(row = 0, column = 0, padx=10, pady=10) 
	historyUI = MoveHistory(root)
	chessboard = ChessBoardGUI(boardFrame, historyUI)
	backendBoard = GameBackend(chess.Board(), chessboard)

	Piece(chessboard, 'rook_b', 'a8')
	Piece(chessboard, 'knight_b', 'b8')
	Piece(chessboard, 'bishop_b', 'c8')
	Piece(chessboard, 'queen_b', 'd8')
	Piece(chessboard, 'king_b', 'e8')
	Piece(chessboard, 'bishop_b', 'f8')
	Piece(chessboard, 'knight_b', 'g8')
	Piece(chessboard, 'rook_b', 'h8')

	root.mainloop()
	print('Exiting...')