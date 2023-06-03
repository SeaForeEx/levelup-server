from django.db import models
from .gamer import Gamer
from .game_type import GameType

class Game(models.Model):

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name='games')
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()

    @property
    def event_info(self):
        """Event specific info"""
        info = []
        for event in self.events.all():
            info.append(event.description)
            info.append(event.date)
            info.append(event.time)
        return info
