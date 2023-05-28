from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer
from levelupapi.models import Game, Gamer, GameType

class GameView(ViewSet):
    """Game view set"""

    def create(self, request): # request = http request
      """Handle POST operations
      Returns
        Response -- JSON serialized game instance
      """
      gamer = Gamer.objects.get(uid=request.data["userId"]) # client side input data from form
      game_type = GameType.objects.get(pk=request.data["gameType"]) # client side input data from form

      game = Game.objects.create(
          title=request.data["title"],
          maker=request.data["maker"],
          number_of_players=request.data["numberOfPlayers"],
          skill_level=request.data["skillLevel"],
          game_type=game_type,
          gamer=gamer,
      ) # request.data is resolve(data) in createGame() on front end
      serializer = GameSerializer(game) # serializer is what gets sent to server
      return Response(serializer.data)

    def retrieve(self, request, pk):
        """GET requests for single game
        Returns JSON serialized game"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET requests for all games
        Returns JSON serialized list of games"""
        games = Game.objects.all()
        
        # filters games based on game type
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
  
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """

        # client is sending info to be updated in the database
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        game_type = GameType.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """DELETE Game"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 2

        
