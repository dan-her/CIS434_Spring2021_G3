from PIL import ImageTk, Image
import tkinter as tk
import chess

class GameBackend():
    def __init__(self, board, gui):
    	self.gui = gui
    	self.start = None
    	self.destination = None
    	self.board = board

    def squareUp(self, event, square):
        if self.start:
            self.destination = square # the total move for the board (i.e. "e2e4")
            if self.destination == self.start:
            	return
            move = self.start.name + self.destination.name
            if (chess.Move.from_uci(move) in self.board.legal_moves): # check if the move is legal
            	x = chess.Move.from_uci(move) # create the move
            	self.board.push(x) # put the move on the board
            	self.destination.piece = Piece(self.gui, self.start.piece.name, square.name)
            	self.start.piece = None # Get rid of piece reference to remove from board
            	self.start = None 
            	self.gui.historyUI.addHistory(move)
            else:
                print("error: bad move")
            print(self.board)
        else:
            self.start = square
            
class ChessBoardGUI():
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

	# Get square from it's name
	def getSquare(self, squareName):
		colNum = Square.SquareLetters.index(squareName[0])
		rowNum = 8 - (int(squareName[1]))
		return self.squares[rowNum][colNum]

# An individial square on a chess board
class Square():
	SquareLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	def __init__(self, chessboard, x, y):
		self.name = Square.SquareLetters[x] + str(8 - y)
		bgcolor = 'gray13'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
		self.piece = None
		self.chessboard = chessboard
		self.canvas = tk.Canvas(chessboard.root, bg = bgcolor, width=64, height=64, highlightthickness=0)  # Canvas with no border to represent each square
		self.canvas.grid(row = y, column = x) # Align to tkinter grid
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

if __name__ == '__main__':
	root = InitWindow()
	boardFrame = tk.Frame(root, padx='5', pady='5') 
	boardFrame.grid(row = 0, column = 0, padx=10, pady=10) 
	historyUI = MoveHistory(root)
	chessboard = ChessBoardGUI(boardFrame, historyUI)
	backendBoard = GameBackend(chess.Board(), chessboard)

	root.mainloop()
	print('Exiting...')
