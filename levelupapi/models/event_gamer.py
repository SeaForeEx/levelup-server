from django.db import models
from .gamer import Gamer
from .event import Event

class EventGamer(models.Model):
    """
    A model that represents the relationship between a Gamer and an Event.
    """

    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    """
    A ForeignKey field that represents a one-to-many relationship between Gamer and EventGamer.
    When a Gamer is deleted, all related EventGamer instances will also be deleted due to the on_delete=models.CASCADE argument.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    """
    A ForeignKey field that represents a one-to-many relationship between Event and EventGamer.
    When an Event is deleted, all related EventGamer instances will also be deleted due to the on_delete=models.CASCADE argument.
    The 'related_name' argument is used to specify the reverse relation from Event to EventGamer, allowing you to access all EventGamer instances related to an Event instance using the 'attendees' attribute.
    """
