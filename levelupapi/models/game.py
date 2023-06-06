from django.db import models
from .gamer import Gamer
from .game_type import GameType

class Game(models.Model):
    """
    A model that represents a game.
    """

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, related_name='games')
    """
    A ForeignKey field that represents a one-to-many relationship between GameType and Game.
    When a GameType is deleted, all related Game instances will also be deleted due to the on_delete=models.CASCADE argument.
    The 'related_name' argument is used to specify the reverse relation from GameType to Game, allowing you to access all Game instances related to a GameType instance using the 'games' attribute.
    """

    title = models.CharField(max_length=50)
    """
    A CharField that stores the title of the game with a maximum length of 50 characters.
    """

    maker = models.CharField(max_length=50)
    """
    A CharField that stores the maker of the game with a maximum length of 50 characters.
    """

    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name='games')
    """
    A ForeignKey field that represents a one-to-many relationship between Gamer and Game.
    When a Gamer is deleted, all related Game instances will also be deleted due to the on_delete=models.CASCADE argument.
    The 'related_name' argument is used to specify the reverse relation from Gamer to Game, allowing you to access all Game instances related to a Gamer instance using the 'games' attribute.
    """

    number_of_players = models.IntegerField()
    """
    An IntegerField that stores the number of players that can play the game.
    """

    skill_level = models.IntegerField()
    """
    An IntegerField that stores the skill level required to play the game.
    """

    @property
    def event_info(self):
        """
        A custom property that returns a list of event-specific information.
        """
        info = []
        for event in self.events.all():
            info.append(event.description)
            info.append(event.date)
            info.append(event.time)
        return info
