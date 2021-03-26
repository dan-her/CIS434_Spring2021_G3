import tkinter as tk

# An individial square on a chess board
class Square():
	def __init__(self, root, x, y):
		self.index = x + y * 8

		bgcolor = 'gray13'
		txtcolor = 'white'
		if (x + y) % 2 == 0:
			bgcolor = 'gray55'
			txtcolor = 'black'

		self.piece = 'none' # Eventually for occupying piece
		self.canvas = tk.Canvas(root, bg = bgcolor, width=64, height=64, border=-2)  # Canvas with no border to represent each square
		self.canvas.create_text(15,10,text=self.getSquareName(), fill = txtcolor) # Square labeled with name of square
		self.canvas.grid(row = y, column = x) # Align to tkinter grid
		self.canvas.bind('<Button-1>', lambda a: print(self.getSquareName() + ' clicked')) # Print name of square when clicked


	def getSquareName(self):
		y = 8 - self.index // 8 # integer division for y on grid, subtracted from 8 for reverse
		x = self.index % 8  # modulo for x on grid
		col = ''
		if x == 0:
			col = 'a'
		if x == 1:
			col = 'b'
		if x == 2:
			col = 'c'
		if x == 3:
			col = 'd'
		if x == 4:
			col = 'e'
		if x == 5:
			col = 'f'
		if x == 6:
			col = 'g'
		if x == 7:
			col = 'h'
		return col + str(y)



def main():
	numrows = 8
	numcols = 8

	root = tk.Tk()
	for i in range(numrows):
		for j in range(numcols):
			Square(root,i,j)
	root.geometry('768x640')
	root.bind('<Escape>', lambda e: root.destroy())
	root.mainloop()
	root.destroy()


if __name__ == '__main__':
	main()
