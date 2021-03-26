import tkinter as tk

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
	SquareLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] # each letter in an array for square AN names

	def __init__(self, root, x, y):
		self.name = Square.getSquareName(x, y)
		bgcolor = 'gray13'
		txtcolor = 'white'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
			txtcolor = 'black'

		self.piece = 'none' # Eventually for occupying piece
		self.canvas = tk.Canvas(root, bg = bgcolor, width=64, height=64, highlightthickness=0)  # Canvas with no border to represent each square
		self.canvas.create_text(15,10,text=self.name, fill = txtcolor) # Square labeled with name of square
		self.canvas.grid(row = y, column = x) # Align to tkinter grid
		self.canvas.bind('<Button-1>', lambda a: print(self.name + ' clicked')) # Print name of square when clicked

	def getSquareName(x, y):
		col = Square.SquareLetters[x]
		return col + str(8 - y)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('768x640')
	chessboard = ChessBoardGUI(root)
	root.bind('<Escape>', lambda e: root.destroy())
	root.mainloop()
	print('Exiting...')
