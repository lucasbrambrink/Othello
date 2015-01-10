from django.shortcuts import render,redirect
from django.views.generic.base import View
from game.othello import Gameboard
from django.http import JsonResponse
import json
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
		g = Gameboard()
		g.import_board(board)
		print(board,move)
		if not g.test_legality(*move):
			return JsonResponse({'e': 'illegal', 'board': g.board})
		g.place(*move)
		g._print()
		return JsonResponse({'board': g.board})
	
