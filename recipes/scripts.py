from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Load your OpenAI API key from an environment variable


# Function to generate a response using GPT-3
def generate_response(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Get user input
user_input = input("Enter your prompt: ")

# Generate a response
response = generate_response(user_input)

# Print the response
print("Response:", response)
