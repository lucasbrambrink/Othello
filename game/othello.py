import copy

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

	def find_legal_moves(self,color):
		empty_cells = [(y,x) for y in range(self.board_size) for x in range(self.board_size) if self.board[y][x] == "O"]
		moves = []
		for cell in empty_cells:
			_try_ = cell + (color,)
			score = self.check_all_directions(*_try_)
			if len(score) > 0:
				moves.append({'cell': cell, 'score': len(score)})
		return moves

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

	def __init__(self,board_instance,color):
		self.board_instance = copy.deepcopy(board_instance)
		self.board = self.board_instance.board
		self.color = color
		self.opposite_color = 'W' if self.color == 'B' else 'B'

	def take_turn(self):
		legal_moves = self.forecast_best_move(self.board)
		# print('ai',legal_moves)
		best_move = sorted(legal_moves,key=lambda x: x['score']-x['human_score'])[-1]
		# print('best_move', best_move)
		return best_move['response'] + (self.color,)

	def find_legal_moves(self):
		empty_cells = [(y,x) for y in range(len(self.board)) for x in range(len(self.board[0])) if self.board[y][x] == "O"]
		moves = []
		for cell in empty_cells:
			_try_ = cell + (self.color,)
			score = self.board_instance.check_all_directions(*_try_)
			if len(score) > 0:
				moves.append({'cell': cell, 'score': len(score)})
		return moves

	@staticmethod
	def __hypothetical_board__(move,color,current_board):
		_move = move['cell'] + (color,)
		hb = Gameboard()
		hb.import_board(current_board)
		hb.place(*_move)
		return hb
			

	def forecast_best_move(self,current_board):
		scenarios = []
		for move in self.find_legal_moves():
			hb = AI.__hypothetical_board__(move,self.color,current_board)
			all_humans_moves = AI(hb,self.color).find_legal_moves()
			# print('human',all_humans_moves)
			for human_move in sorted(all_humans_moves,key=lambda x: x['score'],reverse=True):
				new_hb = AI.__hypothetical_board__(human_move,self.opposite_color,hb.board)
				all_ai_moves = AI(new_hb,self.color).find_legal_moves()
				# print('ai',all_ai_moves)
				if len(all_ai_moves) > 0:
					best_move_in_response = sorted(all_ai_moves,key=lambda x: x['score'],reverse=True)[0]
					scenarios.append({
						'human_score': human_move['score'],
						'response': move['cell'],
						'score': best_move_in_response['score']
						})
				else:
					continue
		return sorted(scenarios,key=lambda x: x['human_score'],reverse=True)



g = Gameboard()
# # g.place(3,2,'B')
# # g.place(2,2,'W')
# ai = AI(g,'W')
# # print(ai.forecast_best_move(g.board))
# ai_move = ai.take_turn()
# print(ai_move)
# print('board')
# g._print()
# new_g = Gameboard()
# new_g.import_board(g.board)
# new_g.place(*ai_move)
# new_g._print()
# # print(ai.take_turn())
print(g.find_legal_moves('W'))

