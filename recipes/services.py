import os
import json
from django.conf import settings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middleware.conf.base')

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


# Load Cameroonian recipes from data.json
def load_cameroonian_recipes():
    try:
        with open(os.path.join('recipes', 'data.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"Error loading recipes file: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from recipes file: {e}")
        return []


cameroonian_recipes = load_cameroonian_recipes()

# Few-shot learning examples
examples = [
    {
        "prompt": "Please provide a detailed recipe for Egusi Soup.",
        "output": """
        {
          "title": "Egusi Soup",
          "description": "A rich and hearty soup made with ground melon seeds, popular in West African cuisine.",
          "prep_time": "15 minutes",
          "cook_time": "45 minutes",
          "total_time": "1 hour",
          "servings": 6,
          "course": "Main Course",
          "cuisine": "Cameroonian",
          "diet": "Gluten Free",
          "author": "Traditional Recipe",
          "ingredients": {
            "main": [
              "1 cup ground egusi (melon seeds)",
              "1 cup spinach, chopped",
              "1 pound beef, cubed",
              "1 cup smoked fish, flaked",
              "1/4 cup crayfish, ground",
              "1/2 cup palm oil",
              "1 large onion, chopped",
              "2 teaspoons ground pepper",
              "Salt to taste",
              "2 seasoning cubes"
            ]
          },
          "instructions": [
            "Blend the egusi with some water to form a paste.",
            "Heat palm oil in a pot and fry the chopped onions until golden brown.",
            "Add the egusi paste and fry for about 10 minutes, stirring constantly.",
            "Add the beef and smoked fish to the pot.",
            "Add water, crayfish, pepper, salt, and seasoning cubes.",
            "Cook for 20 minutes, then add the spinach and cook for another 5 minutes."
          ],
          "notes": [
            "Serve with pounded yam or fufu.",
            "Adjust the thickness of the soup by adding more water if necessary."
          ],
          "nutrition": {
            "calories": "500 kcal",
            "protein": "30 g",
            "fat": "35 g",
            "carbohydrates": "20 g"
          },
          "substitutes": [
            {"original": "1 cup ground egusi (melon seeds)", "substitute": "1 cup ground pumpkin seeds", "reason": "Unavailable"},
            {"original": "1 cup spinach, chopped", "substitute": "1 cup kale, chopped", "reason": "Unavailable"},
            {"original": "1 pound beef, cubed", "substitute": "1 pound tofu, cubed", "reason": "Vegan"},
            {"original": "1/2 cup palm oil", "substitute": "1/2 cup olive oil", "reason": "Dietary Restriction"},
            {"original": "1/4 cup crayfish, ground", "substitute": "1/4 cup dried seaweed, ground", "reason": "Vegan"}
          ]
        }
        """
    },
    {
        "prompt": "Please provide a detailed recipe for Jollof Rice.",
        "output": """
        {
          "title": "Jollof Rice",
          "description": "A popular West African dish made with rice, tomatoes, and spices.",
          "prep_time": "10 minutes",
          "cook_time": "50 minutes",
          "total_time": "1 hour",
          "servings": 8,
          "course": "Main Course",
          "cuisine": "Cameroonian",
          "diet": "Gluten Free",
          "author": "Traditional Recipe",
          "ingredients": {
            "main": [
              "4 cups long grain parboiled rice",
              "6 large tomatoes, blended",
              "4 red bell peppers, blended",
              "2 large onions, chopped",
              "1/4 cup vegetable oil",
              "4 cups chicken stock",
              "1 teaspoon thyme",
              "1 teaspoon curry powder",
              "2 bay leaves",
              "Salt to taste",
              "2 seasoning cubes"
            ]
          },
          "instructions": [
            "Blend tomatoes, red bell peppers, and onions to a smooth paste.",
            "Heat oil in a pot and fry the blended mixture for about 10 minutes.",
            "Add the chicken stock, thyme, curry powder, bay leaves, salt, and seasoning cubes.",
            "Add the rice to the pot and mix well.",
            "Cover the pot and cook on low heat until the rice is done."
          ],
          "notes": [
            "Serve with fried plantains and chicken.",
            "For extra flavor, add a few slices of bell peppers towards the end of cooking."
          ],
          "nutrition": {
            "calories": "400 kcal",
            "protein": "8 g",
            "fat": "10 g",
            "carbohydrates": "70 g"
          },
          "substitutes": [
            {"original": "4 cups long grain parboiled rice", "substitute": "4 cups quinoa", "reason": "Gluten-Free"},
            {"original": "4 cups chicken stock", "substitute": "4 cups vegetable stock", "reason": "Vegetarian"},
            {"original": "1/4 cup vegetable oil", "substitute": "1/4 cup olive oil", "reason": "Healthier option"}
          ]
        }
        """
    }
]


def generate_recipe_description(prompt, model_preference="auto"):
    """Generate a recipe description based on the prompt with improved precision.

    Args:
        prompt (str): Prompt to generate a description from.
        model_preference (str): Model preference ("auto", "gpt-3.5-turbo", "gpt-4").

    Returns:
        str: Generated recipe description or direct example output if prompt matches exactly.
    """
    # Check if the prompt matches any example prompts exactly
    for example in examples:
        if prompt.strip().lower() == example['prompt'].strip().lower():
            return example['output']

    # If no direct match, proceed with dynamic model selection and API call
    model_name = "gpt-3.5-turbo"
    if model_preference == "gpt-4":
        model_name = "gpt-4"
    elif model_preference == "auto":
        model_name = "gpt-4" if len(prompt) > 100 else "gpt-3.5-turbo"

    messages = [
        {"role": "system",
         "content": "You are a helpful assistant skilled in providing authentic Cameroonian recipes."},
    ]

    # Incorporate examples and possibly recipes from the database
    for example in examples:
        messages.append({"role": "user", "content": example['prompt']})
        messages.append({"role": "system", "content": example['output']})

    # Append the user's prompt with detailed request
    detailed_prompt = prompt + "\n\nPlease provide a detailed recipe for a Cameroonian meal in json format, including the following details:\n- Title of the meal\n- Description\n- Prep time\n- Cook time\n- Total time\n- Servings\n- Course\n- Cuisine\n- Diet\n- Author\n- Ingredients\n- Instructions\n- Notes\n- Nutrition"
    messages.append({"role": "user", "content": detailed_prompt})

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            n=1,
            temperature=0.7,  # Example customization
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

    return response.choices[0].message.content


def update_recipe_with_substitutes(recipe, dietary_restrictions):
    """Update the recipe with substitutes based on dietary restrictions.

    Args:
        recipe (dict): The original recipe.
        dietary_restrictions (list): List of dietary restrictions.

    Returns:
        dict: Updated recipe with substitutes.
    """
    substitutes = recipe.get("substitutes", [])
    updated_ingredients = []
    substitute_explanations = []

    for ingredient in recipe["ingredients"]["main"]:
        substitute_found = False
        for sub in substitutes:
            if ingredient.lower() == sub["original"].lower() and any(
                    restriction.lower() in sub["reason"].lower() for restriction in dietary_restrictions):
                updated_ingredients.append(sub["substitute"])
                substitute_explanations.append({
                    "original": ingredient,
                    "substitute": sub["substitute"],
                    "reason": sub["reason"],
                    "explanation": f"The {sub['substitute']} is used as a substitute for {ingredient} due to {sub['reason']}. It provides similar texture and flavor, making it a suitable replacement for this dish."
                })
                substitute_found = True
                break
        if not substitute_found:
            updated_ingredients.append(ingredient)

    recipe["ingredients"]["main"] = updated_ingredients
    recipe["substitute_explanations"] = substitute_explanations
    return recipe

# Example function usage
# prompt = "Please provide a detailed recipe for Egusi Soup."
# dietary_restrictions = ["Vegan"]
#
# recipe_description = generate_recipe_description(prompt)
# recipe = json.loads(recipe_description)
# updated_recipe = update_recipe_with_substitutes(recipe, dietary_restrictions)
#
# print(json.dumps(updated_recipe, indent=2))
