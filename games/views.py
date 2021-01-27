"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer
from datetime import datetime


@api_view(['GET', 'POST'])
def game_list(request):
	if request.method == 'GET':
		games = Game.objects.all()
		games_serializer = GameSerializer(games, many=True)
		return Response(games_serializer.data)
	
	elif request.method == 'POST':
		games_serializer = GameSerializer(data=request.data)
		if games_serializer.is_valid():
			data = games_serializer.data
			dados = Game.objects.filter(name=data['name'])
			
			if dados:
				return Response(
					{'detail': 'this name already exists'},
					status=status.HTTP_400_BAD_REQUEST)

			games_serializer.save()
			return Response(games_serializer.data, status=status.HTTP_201_CREATED)
		return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'POST', 'DELETE'])
def game_detail(request, pk):
	try:
		game = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		games_serializer = GameSerializer(game)
		return Response(games_serializer.data)

	elif request.method == 'PUT':
		games_serializer = GameSerializer(game, data=request.data)		
		if games_serializer.is_valid():
			data = games_serializer.data
			dados = Game.objects.filter(name=data['name'])
			
			if dados:
				return Response({'detail': 'this name already exists'},status=status.HTTP_400_BAD_REQUEST)
				
			else:
				games_serializer.save()
				return Response(games_serializer.data)

		return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		date_now = datetime.today()
		if date_now < game.release_date:
				return Response(
					{'detail':("the game cannot be deleted as it has already been released")},
                    status=status.HTTP_400_BAD_REQUEST)	
		game.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
