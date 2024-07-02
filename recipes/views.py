from django.shortcuts import render
from rest_framework import generics
from .models import Recipe, ChatHistory
from rest_framework import status
from .serializers import RecipeSerializer, ChatbotRequestSerializer, ChatbotResponseSerializer, ChatHistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import GeminiService  # Updated import
from django.http import JsonResponse
from rest_framework.generics import ListAPIView


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

                # Process user message and generate bot response
                gemini_service = GeminiService()  # Updated service
                response_message = gemini_service.generate_response(user_message, temperature=1, max_output_tokens=20000)  # Updated method call

                # Save chat history
                chat_history_data = {
                    'user_message': user_message,
                    'bot_response': response_message,
                }
                chat_history_serializer = ChatHistorySerializer(data=chat_history_data)
                if chat_history_serializer.is_valid():
                    chat_history_serializer.save()
                else:
                    return Response(chat_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Return bot response
                response_serializer = ChatbotResponseSerializer({'response': response_message})
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def test_html_view(request):
    return render(request, 'src/index.html')


class ChatHistoryList(ListAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer