from django.shortcuts import render,redirect
from django.views.generic.base import View
from game.othello import *
from django.http import JsonResponse
import json
import copy
# Create your views here.


class Boardview(View):
	template = 'othello/gameboard.html'

	def get(self,request):
		g = Gameboard()
		return render(request, self.template, {'board': g.board})

class BoardControl(View):

	def get(self,request):
		g = Gameboard()
		return JsonResponse({'board': g.board})

	def post(self,request):
		move = json.loads(request.POST['move'])
		move = list(map(int,move[:-1])) + [move[-1]]
		board = json.loads(request.POST['board'])
		return Controller(move,board).__return__()
	

class Controller:

	def __init__(self,move,board):
		self.g = Gameboard()
		self.g.import_board(board)
		self.move = move
		self.color = move[-1]

	def __return__(self):
		if len(self.g.find_legal_moves(self.color)) == 0:
			return JsonResponse({'g': 'Game Over', 'board': self.g.board})
		if not self.g.test_legality(*self.move):
			return JsonResponse({'e': 'You cannot move there', 'board': self.g.board})
		return self.__ai_move__()

	def __ai_move__(self):
		self.g.place(*self.move)
		self.g._print()
		human_move_board = copy.deepcopy(self.g.board)
		if len(self.g.find_legal_moves(self.color)) == 0:
			return JsonResponse({'g': 'Game Over', 'board': self.g.board})
		ai_color = 'W' if self.color == 'B' else 'B'
		ai = AI(self.g,ai_color)
		ai_move = ai.take_turn()
		self.g.place(*ai_move)
		if len(self.g.find_legal_moves(self.color)) == 0:
			return JsonResponse({'g': 'Game Over', 'board': self.g.board})
		print(human_move_board)
		print(self.g.board)
		return JsonResponse({'first_board': human_move_board, 'board': self.g.board})



