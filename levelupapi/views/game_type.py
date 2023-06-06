"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """
        Handles retrieving a single GameType instance by primary key (pk).
        Parameter: 
            self: The instance of the class on which the method is called
        Args:
            request: The HTTP request object.
            pk: The primary key of the GameType instance to retrieve.

        Returns:
            Response: A serialized GameType instance if found, otherwise a 404 error.
        """
        try:
            # Attempt to get the GameType instance with the given primary key
            game_type = GameType.objects.get(pk=pk)
            # Serialize the retrieved GameType instance
            serializer = GameTypeSerializer(game_type)
            # Return the serialized GameType data as a JSON response
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            # If the GameType instance with the given primary key does not exist, return a 404 error
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests to get all game types.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A serialized list of game types as a JSON response.
        """
        # Get all GameType instances
        game_types = GameType.objects.all()
        # Serialize the retrieved GameType instances with the `GameTypeSerializer`
        # Pass the `many=True` argument to indicate that the serializer should handle multiple instances
        serializer = GameTypeSerializer(game_types, many=True)
        # Return the serialized game types as a JSON response
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    """
    A custom serializer for GameType instances.

    This serializer is a subclass of ModelSerializer, which provides a convenient way
    to create serializers that work with Django models.
    """

    class Meta:
        """
        The Meta class is used to define the serializer's configuration.
        """
        model = GameType  # The GameType model is used as the basis for this serializer
        fields = ('id', 'label')  # Only the 'id' and 'label' fields of the GameType model are serialized
        depth = 1  # The depth of the nested relationships is set to 1
        # depth is useful when you want to include nested objects in your serialized output.

# A ViewSet is a class-based view that combines multiple functionalities for handling common operations, while a Serializer is a tool for converting data types to enable easier data manipulation and rendering. Using both ViewSets and Serializers can help reduce the amount of code you need to write and make your software less error-prone.
