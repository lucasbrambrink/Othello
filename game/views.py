from django.shortcuts import render,redirect
from django.views.generic.base import View
from game.othello import *
from django.http import JsonResponse
from game.models import Users
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
		return JsonResponse({'board': g.board, 'highscores': [{'name': x.name, 'wins': x.wins, 'losses': x.losses, 'ties': x.ties} for x in Users.objects.all()[:5]] })

	def post(self,request):
		move = json.loads(request.POST['move'])
		move = list(map(int,move[:-1])) + [move[-1]]
		board = json.loads(request.POST['board'])
		return Controller(move,board).__return__()
	
class SaveControl(View):

	def get(self,request):
		return JsonResponse({'board': Gameboard().board, 'highscores': [{'name': x.name, 'wins': x.wins, 'losses': x.losses, 'ties': x.ties} for x in Users.objects.all()[:5]] })

	def post(self,request):
		score = json.loads(request.POST['score'])
		name = request.POST['name'].split("=")[1]
		if len(name) > 8:
			name = name[:8]
		user = Users.objects.filter(name=name)
		if len(user) > 0:
			user = user[0]
			user.wins += score['wins']
			user.losses += score['losses']
			user.ties += score['ties']
			user.save()
		else:
			Users.objects.create(name=name,**score)
		return JsonResponse({'board': Gameboard().board, 'highscores': [{'name': x.name, 'wins': x.wins, 'losses': x.losses, 'ties': x.ties} for x in Users.objects.all()[:5]] })


class ShowMoves(View):

	def post(self,request):
		g = Gameboard()
		g.import_board(json.loads(request.POST['board']))
		return JsonResponse({'moves': g.find_legal_moves('W'), 'board': g.board})

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
		ai_color = 'W' if self.color == 'B' else 'B'
		ai = AI(self.g,ai_color)
		print(ai.find_legal_moves())
		if len(ai.find_legal_moves()) == 0:
			return JsonResponse({'g': 'Game Over', 'board': self.g.board})
		ai_move = ai.take_turn()
		self.g.place(*ai_move)
		if len(self.g.find_legal_moves(self.color)) == 0:
			return JsonResponse({'g': 'Game Over', 'board': self.g.board})
		return JsonResponse({'first_board': human_move_board, 'board': self.g.board})


