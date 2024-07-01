from openai import OpenAI
from django.conf import settings
import os


class ChatGPTService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(model="gpt-3.5-turbo",
                                                       messages=[
                                                           {"role": "system", "content": "You are a helpful assistant."},
                                                           {"role": "user", "content": prompt}
                                                       ])

        return response.choices[0].message.content

    def generate_recipe_details(self, prompt):
        if "recipe" in prompt.lower():
            prompt += "\n\nPlease provide a detailed recipe for a Cameroonian meal, including the following details:\n- Title of the meal\n- Instructions\n- Nutritional Value\n- Notes\n- Ethnicity\n- Origin"
        response = self.generate_response(prompt)
        return response