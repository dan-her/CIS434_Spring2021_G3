import tkinter as tk
import chess


# An individial square on a chess board
class Square():
	def __init__(self, root, x, y):
		self.index = x + y * 8

		bgcolor = 'black'
		txtcolor = 'white'
		if (x + y) % 2 == 0:
			bgcolor = 'white'
			txtcolor = 'black'

		self.piece = 'none' # Eventually for occupying piece
		self.canvas = tk.Canvas(root, bg = bgcolor, width=25, height=25) 
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
			root.grid_columnconfigure(j, weight=1)
			root.grid_rowconfigure(i, weight=1)
			Square(root,i,j)
	# root.geometry(768x512)
	root.mainloop()
	root.destroy()

if __name__ == '__main__':
	main()
