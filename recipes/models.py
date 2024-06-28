from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    nutritional_value = models.TextField()
    notes = models.TextField(blank=True, null=True)
    ethnicity = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.timestamp}"
