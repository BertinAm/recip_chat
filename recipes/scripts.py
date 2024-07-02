import google.generativeai as genai
import os

# Configure the API key
api_key = 'AIzaSyD5ah4Mq-QRRH75AgfEIfatJWv7KHdUTuw'
genai.configure(api_key=api_key)

# Get user input
user_input = input("Enter your prompt: ")

try:
    # Remove 'model' argument if not required (check Gemini API documentation)
    response = genai.generate_text(prompt=user_input, temperature=0.5, max_output_tokens=10000)
    print("Response:", response.result)
    print("Response length:", len(response.result))
except Exception as e:
    print(f"An error occurred while generating text: {e}")
