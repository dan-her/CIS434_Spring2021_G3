import math
import time
import sys
import os
import random
import chess
from tkinter import *
from PIL import ImageTk, Image

Color = 1
Images = {}

def PromoteMenu(backend):
	popup = Toplevel()
	popup.title('Promote')
	def promoteKnight():
		backend.doPromote(chess.KNIGHT)
		popup.destroy()
	def promoteBishop():
		backend.doPromote(chess.BISHOP)
		popup.destroy()
	def promoteRook():
		backend.doPromote(chess.ROOK)
		popup.destroy()
	def promoteQueen():
		backend.doPromote(chess.QUEEN)
		popup.destroy()
	Label(popup, text='Promote pawn?').pack()
	Button(popup, text='Knight', command=promoteKnight).pack()
	Button(popup, text='Bishop', command=promoteBishop).pack()
	Button(popup, text='Rook', command=promoteRook).pack()
	Button(popup, text='Queen', command=promoteQueen).pack()

class GameBackend():
	def doPromote(self, piece):
		cSquare1 = chess.parse_square(self.from_square.name)
		cSquare2 = chess.parse_square(self.to_square.name)
		move = chess.Move(from_square = cSquare1, to_square = cSquare2, promotion=piece)
		if (move in self.board.legal_moves): # check if the move is legal
				self.board.push(move) # put the move on the board
				self.from_square = None
				self.to_square.chessboard.RefreshPieces()
				clickt(move)
				if (self.currentOpponent == 1): # call the random opponent
					self.randomMovemaker()
				elif (self.currentOpponent == 2):
					self.quickMovemaker()
				elif (self.currentOpponent == 3):
					self.lazy()
		else:
			print("error: bad move")
			terminal.set("error: bad move")#cg
			self.from_square = None
		if (self.board.is_game_over()):
			print("game over")
			terminal.set("GAME OVER")#cg
		print(self.board)

	def __init__(self, board):
		self.board = board
		self.from_square = None
		self.to_square = None
		self.currentOpponent = 0

	def quickMovemaker(self): # chooses the first move it can (deterministic)
		for move in self.board.legal_moves:
			self.board.push(move)
			clickt(str(move))
			break;

	def randomMovemaker(self): # randomly generates a move
		i = 0
		moves = self.board.legal_moves.count()
		if moves != 0:
			chosen = int(random.randrange(moves))
			for move in self.board.legal_moves:
				if (i == chosen):
					self.board.push(move) # put the move on the board
					clickt(str(move))
					break;
				else:
					i += 1

	def lazy(self): # moves the piece it can move the least
		letterNumbers = {'a':1.0, 'b':2.0, 'c':3.0, 'd':4.0, 'e':5.0, 'f':6.0, 'g':7.0, 'h':8.0} # dict for distance figuring
		chosen = ''
		distance = 999.9 # no legal move will be so long
		distX = 0.0 # values for doing distance calculations
		distY = 0.0
		for move in self.board.legal_moves:
			startxy = [letterNumbers[str(move)[0]], float(str(move)[1])]
			endxy = [letterNumbers[str(move)[2]], float(str(move)[3])]
			
			# diagonals are theoretically more distance than the 4-way straight options, but we want to keep them even
			if ((startxy[0] != endxy[0]) and ( (startxy[0] == (endxy[0] - 1)) or (endxy[0] == (startxy[0]-1)) )):
				distX = 1.0
			else:
				distX = abs( startxy[0]-endxy[0] )
			if ((startxy[1] != endxy[1]) and  ( (startxy[1] == (endxy[1] - 1)) or (endxy[1] == (startxy[1]-1)) )):
				distY = 1.0
			else:
				distY = abs( startxy[1]-endxy[1] ) 
			
			#enforce the distance equalization for diagonals
			if (distX == distY):
				newDistance = distX
			else:
				newDistance = math.sqrt( math.pow( distX, 2 ) +  math.pow( distY, 2 ) )
				
			print("start pos:", startxy[0], startxy[1] , "end pos:", endxy[0], endxy[1])
			print("distX: " , distX, "distY: ", distY)
			print("new distance: ", newDistance)
			if (newDistance == distance): # non-determinism maker
				coinflip = random.randrange(2) # call it
				print("flipped!")
				if (coinflip == 0): # if we get a 0, the old one is replaced
					print("result was 0")
					distance = newDistance
					chosen = move
			if (newDistance < distance): # actually use the shortest one
				distance = newDistance
				chosen = move
		if (chosen != ''):
			self.board.push(chosen) # put the move on the board
			clickt(str(chosen))            
		
	def squareUp(self, square):
		if self.from_square:
			if self.from_square == square:
				self.from_square = None
				return

			self.to_square = square
			cSquare1 = chess.parse_square(self.from_square.name)
			cSquare2 = chess.parse_square(self.to_square.name)

			if 'pawn' in self.from_square.piece.name:
				if (self.to_square.name[1] == '8' and self.board.turn == chess.WHITE) or (self.to_square.name[1] == '1' and self.board.turn == chess.BLACK):
					PromoteMenu(self)
					return

			move = chess.Move(from_square = cSquare1, to_square = cSquare2)
			if (move in self.board.legal_moves): # check if the move is legal
				self.board.push(move) # put the move on the board
				self.from_square.chessboard.DeselectSquare()
				self.from_square.chessboard.UnmarkSquares()
				self.from_square = None
				clickt(move)
				if (self.currentOpponent == 1): # call the random opponent
					self.randomMovemaker()
				elif (self.currentOpponent == 2):
					self.quickMovemaker()
				elif (self.currentOpponent == 3):
					self.lazy()
			else:
				print("error: bad move")
				terminal.set("error: bad move")#cg
				self.from_square = None
			if (self.board.is_game_over()):
				if self.board.is_checkmate():		
					print("game over")
					if (self.board.turn == False):
						terminal.set("GAME OVER: White wins!")#cg
					elif (self.board.turn == True):
						terminal.set("GAME OVER: Black wins!")
				elif self.board.is_stalemate():
					print('stalemate')
					terminal.set('STALEMATE') #cg
				
			print(self.board)
		else:
			if square.piece is not None:
				if (square.piece.name.endswith('w') and self.board.turn == chess.WHITE) or (square.piece.name.endswith('b') and self.board.turn == chess.BLACK): 
					self.from_square = square
					possiblemoves = [move.uci()[2:4] for move in self.board.legal_moves if square.name in move.uci()]
					print(possiblemoves)
					square.chessboard.SelectSquare(square)
					square.chessboard.MarkSquares(possiblemoves)
			


class ChessBoardGUI():
	def __init__(self, root, backend):
		self.backend = backend
		self.root = root
		self.squares = [[Square(self, x, y) for x in range(8)] for y in range(8)]
		self.selected = None
		self.marked = []
		self.RefreshPieces()

	def UnmarkSquares(self):
		self.marked = []

	def DeselectSquare(self):
		self.selected = None

	def SelectSquare(self, square):
		self.selected = square

	def MarkSquares(self, squares):
		for s in squares:
			self.marked.append(self.getSquare(s))

	def RefreshPieces(self):
		for i in range(8):
			for j in range(8):
				self.squares[i][j].canvas.delete('all')
				self.squares[i][j].piece = None

		pieces = self.backend.board.piece_map()
		for k,v in pieces.items():
			name = chess.square_name(k)
			color = v.color
			kind = v.piece_type

			if kind == chess.KING:
				piece = 'king'
			elif kind == chess.QUEEN:
				piece = 'queen'
			elif kind == chess.ROOK:
				piece = 'rook'
			elif kind == chess.KNIGHT:
				piece = 'knight'
			elif kind == chess.BISHOP:
				piece = 'bishop'
			elif kind == chess.PAWN:
				piece = 'pawn'

			if color == chess.WHITE:
				piece += '_w'
			else:
				piece += '_b'


			self.getSquare(name).piece = Piece(self, piece, name)

			
		if self.selected:
			self.selected.canvas.create_image(32, 32, image=Images['selector'])
		if self.marked:
			for square in self.marked:
				square.canvas.create_image(32, 32, image=Images['marker'])




	# Convert AN name of square into array indices and returns square
	def getSquare(self, squareName):
		colNum = Square.SquareLetters.index(squareName[0])
		rowNum = 8 - (int(squareName[1]))
		return self.squares[rowNum][colNum]

# An individial square on a chess board
class Square():
	SquareLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	def onClick(self, event):
		backendBoard.squareUp(self)
		self.chessboard.RefreshPieces()

	def __init__(self, chessboard, x, y):
		self.name = Square.getSquareName(x, y)
		bgcolor = 'gray13'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
		self.piece = None
		self.chessboard = chessboard
		# Canvas with no border to represent each square
		self.canvas = Canvas(chessboard.root, bg = bgcolor, width=64, height=64, highlightthickness=0) 
		# Align to tkinter grid
		self.canvas.grid(row = y, column = x) 
		self.canvas.bind('<Button-1>', self.onClick) 

	def getSquareName(x, y):
		col = Square.SquareLetters[x]
		return col + str(8 - y)

	# Get grid x/y coords from a square
	def getCoords(self):
		colNum = Square.SquareLetters.index(self.name[0])
		rowNum = 8 - (int(self.name[1]))
		return colNum, rowNum

class Piece():
	def __init__(self, chessboard, pieceName, squareName):
		self.name = pieceName
		self.image = Images[self.name]
		chessboard.getSquare(squareName).canvas.create_image(32,32,image=self.image)
		chessboard.getSquare(squareName).piece = self

def InitImages():
	pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
	for p in pieces:
		bName = p + '_b'
		wName = p + '_w'		
		imageb = Image.open('assets//' + bName + '.png')
		imageb.thumbnail((48, 48))
		tkImageB = ImageTk.PhotoImage(imageb)
		imagew = Image.open('assets//' + wName + '.png')
		imagew.thumbnail((48, 48))
		tkImageW = ImageTk.PhotoImage(imagew)
		Images[bName] = tkImageB
		Images[wName] = tkImageW

	selector = Image.open('assets//selector.png')
	selector.thumbnail((56, 56))
	Images['selector'] = ImageTk.PhotoImage(selector)

	marker = Image.open('assets//marker.png')
	marker.thumbnail((56, 56))
	Images['marker'] = ImageTk.PhotoImage(marker)

def InitWindow():
	root = Tk()
	root.geometry('768x640')
	root.title('Chess')
	root.configure(background='grey7')
	root.bind('<Escape>', lambda e: root.destroy())
	return root

def clickt(item):
	global Color
	mylist.insert(ACTIVE, item)
	if (Color == 1):
		terminal.set("Turn: Black") 
		Color = 0
	else:
		terminal.set("Turn: White")
		Color = 1
		
def opponentSet(ID):
	backendBoard.currentOpponent = ID

def reset():
	backendBoard.board.reset()
	chessboard.RefreshPieces()
	while mylist.size() != 0:
		mylist.delete(mylist.size()-1)
	global Color
	Color = 1
	terminal.set("Turn: White")

def tryundo():
	try:
		backendBoard.board.pop()
		mylist.delete(mylist.size()-1)
		global Color
		if backendBoard.currentOpponent > 0:
			backendBoard.board.pop()
			mylist.delete(mylist.size()-1)
		elif Color == 1:
			terminal.set("Turn: Black") 
			Color = 0
		else:
			terminal.set("Turn: White")
			Color = 1
	except IndexError:
		return
	else:
		chessboard.RefreshPieces()
		
if __name__ == '__main__':
	root = InitWindow()
	InitImages()
	boardFrame = Frame(root) 
	boardFrame.grid(row = 0, column = 0, padx=10, pady=10) 
	backendBoard = GameBackend(chess.Board()) # init backend board
	chessboard = ChessBoardGUI(boardFrame, backendBoard)
	
	historyFrame = LabelFrame(root, text = "Move History") 
	historyFrame.grid(row = 0, column = 1, padx=10, pady=10)
	scrollbar = Scrollbar(historyFrame, orient = VERTICAL)
	mylist = Listbox(historyFrame, yscrollcommand = scrollbar.set)
	scrollbar.config(command = mylist.yview)
	scrollbar.pack(side = RIGHT, fill = Y)
	mylist.pack(side = LEFT, fill = BOTH)
	
	mb = Menu(root)
	gamemenu = Menu(mb)
	gamemenu.add_command(label='reset', command=lambda: reset())
	gamemenu.add_command(label='exit', command=lambda: sys.exit())
	mb.add_cascade(menu=gamemenu, label='Game')
	opponentsmenu = Menu(mb)
	opponentsmenu.add_checkbutton(label='player',  command=lambda: opponentSet(0))
	opponentsmenu.add_checkbutton(label='random',  command=lambda: opponentSet(1))
	opponentsmenu.add_checkbutton(label='ordered', command=lambda: opponentSet(2))
	opponentsmenu.add_checkbutton(label='lazy',    command=lambda: opponentSet(3))
	mb.add_cascade(menu=opponentsmenu, label='Opponents')
	root.configure(menu=mb) 

	terminalFrame = LabelFrame(root, text = "Terminal")#cg
	terminalFrame.grid(row = 1, column = 0, padx=10, pady=10)#cg
	terminal = StringVar()#cg
	label = Label(terminalFrame, width = 64, height = 1, textvariable=terminal)#cg
	label.pack()#cg
	terminal.set("Turn: White")#cg

	Button(historyFrame, text='Undo Move', command=tryundo).pack()
	
	root.mainloop()
	print('Exiting...')
