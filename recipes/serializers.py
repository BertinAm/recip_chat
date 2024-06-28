from rest_framework import serializers
from .models import Recipe, ChatHistory


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'instructions', 'nutritional_value', 'notes', 'ethnicity', 'origin']


class ChatbotRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=1000)


class ChatbotResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'user_message', 'bot_response', 'timestamp']