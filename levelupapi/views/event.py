"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Game, Gamer, EventGamer
from django.db.models import Count, Q


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
        # retrieves the HTTP_AUTHORIZATION header from the request's metadata and assigns it to the variable uid
        uid = request.META.get('HTTP_AUTHORIZATION')
        # retrieves the Gamer object with the uid retrieved from the request
        gamer = Gamer.objects.get(uid=uid)
        # retrieves all Event objects and annotates them with two additional fields: attendees_count and joined
        events = Event.objects.annotate(
            # the count of all attendees for each event
            attendees_count=Count('attendees'),
            # the count of attendees that match the gamer retrieved from the request
            joined=Count(
                'attendees',
                filter=Q(attendees__gamer=gamer)
            )
            # In this case, attendees is the field we are looking up, and gamer is the field we are filtering on. The double underscore notation is used to indicate that we are performing a lookup on the attendees field to filter the results based on the gamer field. This allows us to retrieve only the Event objects where the related attendee has a matching gamer.
        )
        # for event in events:
        #     # Check to see if there is a row in the Event Games table that has the passed in gamer and event
        #     event.joined = len(EventGamer.objects.filter(
        #     gamer=gamer, event=event)) > 0
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
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
        
        gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        event_gamer = EventGamer.objects.filter(gamer=gamer, event=event)
        event_gamer.delete()
        return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)
        

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    attendees_count = serializers.IntegerField(default=None)
    time = serializers.TimeField(format="%I:%M %p")
    date = serializers.DateField(format="%B %d, %Y")
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'joined', 'attendees_count')
        depth = 2
