from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, ChatHistory
from .serializers import RecipeSerializer, ChatbotRequestSerializer, ChatbotResponseSerializer, ChatHistorySerializer
from .services import generate_recipe_description  # Updated import


class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class ChatbotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ChatbotRequestSerializer(data=request.data)
            if serializer.is_valid():
                user_message = serializer.validated_data['message']
                # Assuming generate_response is updated to handle the new service logic
                response_message = generate_recipe_description(user_message)
                chat_history_data = {
                    'user_message': user_message,
                    'bot_response': response_message,
                }
                chat_history_serializer = ChatHistorySerializer(data=chat_history_data)
                if chat_history_serializer.is_valid():
                    chat_history_serializer.save()
                    response_serializer = ChatbotResponseSerializer({'response': response_message})
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(chat_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateRecipeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        model_preference = request.data.get('model_preference', 'auto')
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recipe_description = generate_recipe_description(prompt, model_preference)
            return Response({"recipe_description": recipe_description}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def test_html_view(request):
    return render(request, 'src/index.html')


class ChatHistoryList(generics.ListAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer
