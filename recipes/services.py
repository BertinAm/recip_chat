import google.generativeai as genai
from django.conf import settings
import os


class GeminiService:
    def __init__(self):
        self.api_key = 'AIzaSyD5ah4Mq-QRRH75AgfEIfatJWv7KHdUTuw'
        genai.configure(api_key=self.api_key)

    def generate_response(self, prompt, temperature=1, max_output_tokens=20000):  # Increase max_output_tokens
        try:
            # Generate a response
            response = genai.generate_text(prompt=prompt, temperature=temperature, max_output_tokens=max_output_tokens)

            # Print response length for debugging (optional)
            print(f"Generated response length: {len(response.result)}")

            # Return only the generated text
            return response.result
        except Exception as e:
            # Handle API error, log or return a default message
            print(f"An error occurred while calling Gemini API: {e}")
            return "An error occurred while generating the response."

    def generate_recipe_details(self, prompt):
        if "recipe" in prompt.lower():
            prompt += "\n\nPlease provide a detailed recipe for a Cameroonian meal, including the following details:\n- Title of the meal\n- Instructions\n- Nutritional Value\n- Notes\n- Ethnicity\n- Origin"
        response = self.generate_response(prompt)
        return response
