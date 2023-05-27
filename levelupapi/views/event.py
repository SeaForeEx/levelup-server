"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Game, Gamer, EventGamer


class EventView(ViewSet):
    """Level up events view"""
    
    def create(self, request):
        """POST Event
        Returns JSON instance
        """
        organizer = Gamer.objects.get(uid=request.data["userId"])
        game = Game.objects.get(pk=request.data["game"])
        
        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer,
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Update Event
        Returns Empty Body with 204 status
        """
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(uid=request.data["userId"])
        event.game = game
        event.organizer = organizer
        event.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(uid=request.data["userId"])
        event = Event.objects.get(pk=pk)
        EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """DELETE Event"""
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Leave an event"""
        
        gamer = Gamer.objects.get(uid=request.data["userId"])
        event = Event.objects.get(pk=pk)
        event_gamer = EventGamer.objects.filter(gamer=gamer, event=event)
        event_gamer.delete()
        return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)
        

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    time = serializers.TimeField(format="%I:%M %p")
    date = serializers.DateField(format="%B %d, %Y")
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 2
