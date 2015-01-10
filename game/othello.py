
class Gameboard:

	def __init__(self):
		self.board_size = 8
		self.board = [['O' for y in range(0,self.board_size)] for x in range(0,self.board_size)]
		self.starting_position()

	def _print(self):
		for c in self.board:
			print(c)

	def import_board(self,board):
		self.board = board

	def starting_position(self):
		self.board[3][3] = 'W'
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[4][3] = 'B'

	def place(self,y,x,color):
		self.board[y][x] = color
		for c in self.check_all_directions(y,x,color):
			self.board[c[0]][c[1]] = c[2]
		return True  
	
	def test_legality(self,y,x,color):
		if len(self.check_all_directions(y,x,color)) == 0:
			return False
		return True

	def check_all_directions(self,y,x,color):
		opposite_color = 'W' if color == 'B' else 'B'
		all_directions = [(1,0),(-1,0),(1,1),(-1,1),(-1,-1),(1,-1),(0,1),(0,-1)]
		coordinates = []
		for d in all_directions:
			i,j = y+d[0],x+d[1]
			to_switch = []
			while 0 <= i < self.board_size and 0 <= j < self.board_size:
				if self.board[i][j] == opposite_color:
					to_switch.append([i,j,color])
					i += d[0]
					j += d[1]
				elif self.board[i][j] == color:
					if len(to_switch) > 0:
						coordinates.append(to_switch)
					break
				else:
					break
		return [y for x in coordinates for y in x]


class AI:

	def __init__(self,color):
		self.color = color

	def take_turn(self,board_instance):
		self.board_instance = board_instance
		self.board = board_instance.board
		legal_moves = self.find_legal_moves()
		best_move = sorted(legal_moves,key=lambda x: x['score'])[-1]
		return best_move

	def find_legal_moves(self):
		empty_cells = [(y,x) for y in range(len(self.board)) for x in range(len(self.board[0])) if self.board[y][x] == "O"]
		moves = []
		for cell in empty_cells:
			score = board_instance.check_all_directions(*[cell+self.color])
			if len(score) > 0:
				moves.append({'cell': cell, 'score': score})
		return moves


g = Gameboard()
# g.place(3,2,'B')
# g.place(2,2,'W')
g._print()

