import tkinter as tk
from tkinter import *
import chess
from PIL import ImageTk, Image

# global variables
squaresCount = 0 # for gameBackend
initPos = '' # for gameBackend



class gameBackend():
    def __init__(self, board):
        self.board = board
        print("Whee!")
    def squareUp(self, square):
        global initPos
        global squaresCount
        if (squaresCount == 1):
            initPos += square # the total move for the board (i.e. "e2e4")
            squaresCount = 0
            print(initPos)
            if (chess.Move.from_uci(initPos) in self.board.legal_moves): # check if the move is legal
                x = chess.Move.from_uci(initPos) # create the move
                self.board.push(x) # put the move on the board
                clickt(initPos)
            else:
                print("error: bad move")
            if (self.board.is_checkmate()):
                print("g'over")
            print(self.board)
        else:
            initPos = square
            squaresCount = 1
            
        

class ChessBoardGUI():
	def __init__(self, root):
		self.squares = [[Square(root, x, y) for x in range(8)] for y in range(8)]

	# Convert AN name of square into array indices and returns square
	def getSquare(self, squareName):
		colNum = Square.SquareLetters.index(squareName[0])
		rowNum = 8 - (int(squareName[1]))
		return self.squares[rowNum][colNum]

# An individial square on a chess board
class Square():
	SquareLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	def __init__(self, root, x, y):
		self.name = Square.getSquareName(x, y)
		bgcolor = 'gray13'
		txtcolor = 'white'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
			txtcolor = 'black'
		self.piece = 'none' # Eventually for occupying piece
		self.canvas = tk.Canvas(root, bg = bgcolor, width=64, height=64, highlightthickness=0)  # Canvas with no border to represent each square
		# self.canvas.create_text(15,10,text=self.name, fill = txtcolor) # what did this do?
		self.canvas.grid(row = y, column = x) # Align to tkinter grid
		self.canvas.bind('<Button-1>', lambda a: backendBoard.squareUp(self.name)) # Send name of square to the fcn that controls the board 
	def getSquareName(x, y):
		col = Square.SquareLetters[x]
		return col + str(8 - y)

	# Get grid x/y coords from a square
	def getCoords(self):
		colNum = Square.SquareLetters.index(self.name[0])
		rowNum = 8 - (int(self.name[1]))
		return colNum, rowNum

class Piece():
	def __init__(self,root, chessboard, pieceName, squareName):
		path = "assets//"+pieceName + '.png'
		image = Image.open(path)
		image.thumbnail((48, 48)) # Resize the piece to fit (can also use image.resize I believe)
		self.img = ImageTk.PhotoImage(image)
		chessboard.getSquare(squareName).canvas.create_image(32,32,image=self.img)

def InitWindow():
	root = tk.Tk()
	root.geometry('768x640')
	root.title('Chess')
	#root.iconbitmap('assets//icon.ico') # this currently doesn't exist, so i commented out the line that refers to it
	root.configure(background='grey7')
	root.bind('<Escape>', lambda e: root.destroy())
	return root
    
def clickt(item): # authored by curtis gach
    mylist.insert(END, item) # authored by curtis gach

if __name__ == '__main__':
	root = InitWindow()
	backendBoard = gameBackend(chess.Board()) # init backend board
	boardFrame = Frame(root, padx='5', pady='5') # authored by curtis gach
	boardFrame.grid(row = 0, column = 0, padx=10, pady=10) # authored by curtis gach
	chessboard = ChessBoardGUI(boardFrame)
	historyFrame = LabelFrame(root, text="history frame", padx = 5, pady = 5) # authored by curtis gach
	historyFrame.grid(row = 0, column = 1, padx=10, pady=10) # authored by curtis gach
	scrollbar = Scrollbar(historyFrame) # authored by curtis gach
	scrollbar.pack(side = RIGHT, fill = Y) # authored by curtis gach
	mylist = Listbox(historyFrame, yscrollcommand = scrollbar.set) # authored by curtis gach
	mylist.pack(side = LEFT, fill = BOTH) # authored by curtis gach
	p1w = Piece(root, chessboard, 'pawn_w', 'a2') # add pieces in default (original) organization, white starts here
	p2w = Piece(root, chessboard, 'pawn_w', 'b2') # there's definitely a better way to do this, but this is a band-aid solution that will hopefully be replaced later
	p3w = Piece(root, chessboard, 'pawn_w', 'c2')
	p4w = Piece(root, chessboard, 'pawn_w', 'd2')
	p5w = Piece(root, chessboard, 'pawn_w', 'e2')
	p6w = Piece(root, chessboard, 'pawn_w', 'f2')
	p7w = Piece(root, chessboard, 'pawn_w', 'g2')
	p8w = Piece(root, chessboard, 'pawn_w', 'h2')
	r1w = Piece(root, chessboard, 'rook_w', 'a1')
	k1w = Piece(root, chessboard, 'knight_w', 'b1')
	b1w = Piece(root, chessboard, 'bishop_w', 'c1')
	q0w = Piece(root, chessboard, 'queen_w', 'd1')
	k0w = Piece(root, chessboard, 'king_w', 'e1')
	b2w = Piece(root, chessboard, 'bishop_w', 'f1')
	k2w = Piece(root, chessboard, 'knight_w', 'g1')
	r2w = Piece(root, chessboard, 'rook_w', 'h1')
	
	p1b = Piece(root, chessboard, 'pawn_b', 'a7') # black starts here
	p2b = Piece(root, chessboard, 'pawn_b', 'b7')
	p3b = Piece(root, chessboard, 'pawn_b', 'c7')
	p4b = Piece(root, chessboard, 'pawn_b', 'd7')
	p5b = Piece(root, chessboard, 'pawn_b', 'e7')
	p6b = Piece(root, chessboard, 'pawn_b', 'f7')
	p7b = Piece(root, chessboard, 'pawn_b', 'g7')
	p8b = Piece(root, chessboard, 'pawn_b', 'h7')
	r1b = Piece(root, chessboard, 'rook_b', 'a8')
	k1b = Piece(root, chessboard, 'knight_b', 'b8')
	b1b = Piece(root, chessboard, 'bishop_b', 'c8')
	q0b = Piece(root, chessboard, 'queen_b', 'd8')
	k0b = Piece(root, chessboard, 'king_b', 'e8')
	b2b = Piece(root, chessboard, 'bishop_b', 'f8')
	k2b = Piece(root, chessboard, 'knight_b', 'g8')
	r2b = Piece(root, chessboard, 'rook_b', 'h8')
	
	root.mainloop()
	print('Exiting...')
