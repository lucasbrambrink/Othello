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

	@staticmethod
	def border_scewing(moves,key):
		corners = [(0,0),(7,0),(0,7),(7,7)]
		for x in moves:
			if x[key] in corners:
				x['score'] += (20+max(x['score']),)
			elif 0 in x[key] or 7 in x[key]:
				x['score'] += (10+max(x['score']),)
		return moves

	@staticmethod
	def border_scoring(moves):
		corners = [(0,0),(7,0),(0,7),(7,7)]
		for x in moves:
			if x['cell'] in corners:
				x['score'] += 20
			elif 0 in x['cell'] or 7 in x['cell']:
				x['score'] += 10
		return moves

	@staticmethod
	def finalize_scoring(moves):
		for x in moves:
			x['agg_score'] = max(x['score'])-max(x['human_score'])
		return moves

	@staticmethod
	def __min_max__(moves,key):
		return min([max(x[key]) for x in moves]), max([max(x[key]) for x in moves])

	@staticmethod
	def adjust_for_performance(moves):
		min_hs,max_hs = AI.__min_max__(moves,'human_score')
		min_sc,max_sc = AI.__min_max__(moves,'score')
		print(min_hs,max_hs)
		print(min_sc,max_sc)
		for move in moves:
			if max(move['human_score']) == min_hs:
				move['agg_score'] += 2
			elif max(move['human_score']) == max_hs:
				move['agg_score'] -= 2
			if max(move['score']) == max_sc:
				move['agg_score'] += 2
			elif max(move['score']) == min_sc:
				move['agg_score'] -= 1
		return moves

	def print_array(self,name,array):
		print(name)
		min_hs,max_hs = AI.__min_max__(array,'human_score')
		min_sc,max_sc = AI.__min_max__(array,'score')
		print("min,max :: ",min_hs,max_hs)
		print("min,max :: ",min_sc,max_sc)
		for c in array:
			print("      ",c['response'])
			print("             ",c['score'])
			print("             ",c['human_score'])
			print('')
			if 'agg_score' in c:
				print("          ",c['agg_score'])
		print('\n\n\n\n')

	def take_turn(self):
		legal_moves = self.forecast_best_move(self.board)
		corner_adjusted_moves = self.border_scewing(copy.deepcopy(legal_moves),'response')
		weighted_moves = self.finalize_scoring(copy.deepcopy(corner_adjusted_moves))
		adjusted_moves = self.adjust_for_performance(copy.deepcopy(weighted_moves))
		self.print_array('legal_moves',legal_moves)
		self.print_array('corner_adjusted_moves',corner_adjusted_moves)
		self.print_array('weighted_moves',weighted_moves)
		self.print_array('adjusted_moves',adjusted_moves)
		best_move = sorted(adjusted_moves,key=lambda x: x['agg_score'],reverse=True)[0]
		print('best_move', best_move)
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
			all_humans_moves = AI(hb,self.opposite_color).find_legal_moves()
			if len(all_humans_moves) == 0:
				scenarios.append({
					'human_score': (0,),
					'response': move['cell'],
					'score': (move['score'],)
					})
			else:
				all_humans_moves = self.border_scoring(all_humans_moves)
				for human_move in sorted(all_humans_moves,key=lambda x: x['score'],reverse=True):
					# print('human',human_move)	
					new_hb = AI.__hypothetical_board__(human_move,self.opposite_color,hb.board)
					all_ai_moves = AI(new_hb,self.color).find_legal_moves()
					# for c in all_ai_moves:
					# 	print(c)
					if len(all_ai_moves) > 0:
						best_move_in_response = sorted(all_ai_moves,key=lambda x: x['score'],reverse=True)[0]
						obj = [x for x in scenarios if x['response'] == move['cell']]
						if len(obj) > 0:
							obj[0]['score'] += (best_move_in_response['score'],) 
							obj[0]['human_score'] += (human_move['score'],)
						else:
							scenarios.append({
							'human_score': (human_move['score'],),
							'response': move['cell'],
							'score': (best_move_in_response['score'],)
							})
		if len(scenarios) == 0:
			best_last_move = sorted(self.find_legal_moves(), lambda x: x['score'],reverse=True)[0]
			scenarios.append({
					'human_score': (0,),
					'response': best_last_move['cell'],
					'score': (best_last_move['score'],)
					})
		for c in sorted(scenarios,key=lambda x: max([y for y in x['human_score']])):
			print(c)
		return scenarios



# g = Gameboard()
# ai = AI(g,'W')
# ai.take_turn()

## Bug Fix ##
"""
Occasional error about type checking in line 151

"""
# g = Gameboard()
# g.import_board([['B', 'B', 'B', 'B', 'B', 'B', 'O', 'W'],
# ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
# ['B', 'O', 'W', 'B', 'B', 'W', 'B', 'W'],
# ['B', 'B', 'W', 'B', 'B', 'B', 'B', 'W'],
# ['B', 'W', 'B', 'B', 'B', 'B', 'B', 'W'],
# ['B', 'B', 'W', 'B', 'B', 'B', 'B', 'W'],
# ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
# ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'O']])
# g._print()
# print(g.find_legal_moves('W'))
# print(g.find_legal_moves('B'))
# move = (2,1,'B')
# g.place(*move)
# g._print()


g = Gameboard()
def AI_battle(board):
	ai1 = AI(g,'W')
	ai2 = AI(g,'B')
	if len(ai1.find_legal_moves()) == 0:
		g._print()
		return None
	ai1_move = ai1.take_turn()
	g.place(*ai1_move)
	if len(ai2.find_legal_moves()) == 0:
		g._print()
		return None
	ai2_move = ai2.take_turn()
	g.place(*ai2_move)
	return AI_battle(g)

# AI_battle(g)
		










