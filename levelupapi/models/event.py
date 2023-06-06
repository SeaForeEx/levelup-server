from django.db import models
from .game import Game
from .gamer import Gamer

class Event(models.Model):
    """
    A model that represents an event.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    """
    A ForeignKey field that represents a one-to-many relationship between Game and Event.
    When a Game is deleted, all related Event instances will also be deleted due to the on_delete=models.CASCADE argument.
    The 'related_name' argument is used to specify the reverse relation from Game to Event, allowing you to access all Event instances related to a Game instance using the 'events' attribute.
    """

    description = models.CharField(max_length=50)
    """
    A CharField that stores a description of the event with a maximum length of 50 characters.
    """

    date = models.DateField(auto_now=False, auto_now_add=False)
    """
    A DateField that stores the event date. The date is not automatically set to the current date (auto_now=False) and is not automatically added when a new event is created (auto_now_add=False).
    """

    time = models.TimeField()
    """
    A TimeField that stores the event time.
    """

    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    """
    A ForeignKey field that represents a one-to-many relationship between Gamer and Event.
    When a Gamer is deleted, all related Event instances will also be deleted due to the on_delete=models.CASCADE argument.
    """
    
    @property
    def joined(self):
        """Custom Property that returns 'joined' attribute"""
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
        
        # The double underscores are used to create custom property and setter methods for the joined attribute
    
