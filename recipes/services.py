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
          }
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
          }
        }
        """
    },
    {
        "prompt": "Please provide me with the recipe for pepper soup",
        "output": """
         {
          "title": "African Pepper Sauce",
          "description": "This African Pepper Sauce is a hot sauce made with hot peppers, spices, and herbs. The perfect accompaniment to any meal!",
          "prep_time": "15 minutes",
          "cook_time": "30 minutes",
          "total_time": "45 minutes",
          "servings": 20,
          "course": "Appetizer",
          "cuisine": "African",
          "diet": ["Gluten Free", "Vegan", "Vegetarian"],
          "author": "Precious",
          "ingredients": [
            "6 roma tomatoes, cut into quarters",
            "1 red onion, cut into chunks",
            "4 habanero peppers, stems removed",
            "6 sprigs parsley, rinsed, hard stems removed",
            "6 sprigs basil, rinsed, leaves plucked from hard stems",
            "2 inches ginger root, peeled and diced",
            "6 cloves garlic, peeled",
            "1 teaspoon salt",
            "2 tablespoons olive oil",
            "1 teaspoon dried thyme (optional)",
            "1 teaspoon dried basil (optional)"
          ],
          "instructions": [
            "Add all the ingredients to a blender and blend into a paste.",
            "Pour the pepper mixture into a small pot. Add in the olive oil and dried herbs (if using). Bring the pot to a boil on medium heat and let it simmer on low heat for about 20 minutes, stirring from time to time to prevent burning.",
            "Adjust the salt if necessary and turn off the heat.",
            "Store pepper sauce in small airtight jars for up to a week in the refrigerator."
          ],
          "notes": [
            "The best way to adjust the level of heat in this pepper sauce is to reduce the quantity of habanero peppers used. For a more mild sauce, use two or three peppers instead of four.",
            "This sauce makes a great marinade for grilled meats or fish.",
            "For a thicker sauce, let it cook for a longer time, or reduce the quantity of tomatoes used."
          ],
          "nutrition": {
            "calories": "14 kcal",
            "carbohydrates": "3 g",
            "protein": "1 g",
            "fat": "1 g",
            "saturated_fat": "0.1 g",
            "polyunsaturated_fat": "0.2 g",
            "monounsaturated_fat": "0.7 g",
            "sodium": "118 mg",
            "potassium": "106 mg",
            "fiber": "1 g",
            "sugar": "2 g",
            "vitamin_a": "325 IU",
            "vitamin_c": "9 mg",
            "calcium": "12 mg",
            "iron": "0.3 mg"
          }
        }
        """
    },
    {
        "prompt": "Please provide me with a recipe for cabbage and beef stew",
        "output": """
        {
          "title": "Cabbage and Beef Stew",
          "description": "Hearty stew with cabbage and beef that can be served over rice or with your favorite starchy sides. It is garlicky meaty, so good!",
          "prep_time": "30 minutes",
          "cook_time": "30 minutes",
          "total_time": "1 hour",
          "servings": "6 servings",
          "author": "Precious",
          "ingredients": [
            "1 head cabbage, 4 pounds or use 2 small cabbages equaling about 4 pounds",
            "1 pound beef for stew or use chuck roast",
            "2 medium carrots cut into matchsticks",
            "10 garlic cloves peeled, mashed into a paste or blended",
            "2 inches ginger root, mashed into a paste or blended",
            "½ cup neutral oil (used peanut oil)",
            "1 medium onion, chopped",
            "10 medium tomatoes, diced (use Roma if available)",
            "1 teaspoon ground white pepper",
            "Salt to taste",
            "2 teaspoons chicken bouillon powder"
          ],
          "instructions": [
            "Shred the cabbage. Cut the cabbage into wedges. About 4-6 wedges or up to 8 wedges for a larger cabbage. Shred by slicing the wedges on the slice side of a standard box grater.",
            "Gather any loose cabbage leaves and slice them.",
            "Blanche the cabbage. Bring water to a boil in a large pot. Add 2 teaspoons of salt. Put the cabbage into the pot. Push in with a wooden spoon to completely submerge. Turn off the heat, cover the pot and let it sit for 5 minutes.",
            "Rinse the cabbage. Pass cabbage through a colander. Immediately rinse with cold water to stop the cooking process. Squeeze out excess water from cabbage and set aside.",
            "Cook the beef. Place beef in a pot. Add half a teaspoon of salt, a quarter teaspoon of ground white pepper and 2 tablespoons of the chopped onions. Add one cup of water. Cook beef for 8-10 minutes or until tender.",
            "Sauté onions and tomatoes. Place a pot on high heat. Add oil. Heat up until shimmering. Add onions and sauté for one minute. Add diced tomatoes and cook while stirring from time to time for 15 minutes. It is important to stir tomatoes consistently so they don't burn. The tomatoes will shrink considerably as they cook.",
            "Add aromatics, carrots and beef. Add garlic and ginger paste, then stir for 1 minute. Add white pepper, and stir for 1 minute. Add sliced carrots, stir for 2 minutes. Add back beef with a quarter cup of its broth. Stir and let it simmer for 2 minutes.",
            "Add cabbage and season to taste. Add the cabbage to the pot. Stir well to combine. Add 2 teaspoons of chicken bouillon powder and stir well to combine. Add salt to taste and stir well to combine. I added a loose teaspoon of salt. Let everything simmer together for 2-5 minutes. Taste and adjust seasoning according to taste. Add some cayenne pepper if want some heat.",
            "Serve warm. Serve with steamed rice, plantains or roasted potatoes."
          ],
          "notes": [
            "Try the following variations for your Cabbage and Beef Stew:",
            "Spicy - Add some cayenne pepper when adding the white pepper or for just mildly spicy, add some crushed red pepper flakes instead. If you want it super spicy, blend one habanero pepper and put it.",
            "Different Protein - Try making beef and cabbage stew with chicken instead or any other protein you like.",
            "More Sauce - If you like your cabbage stew saucier, add all of the beef stock to the stew and let it simmer with the other ingredients."
          ],
          "nutrition": {
            "calories": "355 kcal",
            "carbohydrates": "19 g",
            "protein": "21 g",
            "fat": "23 g",
            "saturated_fat": "3 g",
            "polyunsaturated_fat": "6 g",
            "monounsaturated_fat": "13 g",
            "trans_fat": "0.1 g",
            "cholesterol": "47 mg",
            "sodium": "250 mg",
            "potassium": "884 mg",
            "fiber": "6 g",
            "sugar": "10 g",
            "vitamin_a": "4407 IU",
            "vitamin_c": "74 mg",
            "calcium": "108 mg",
            "iron": "3 mg"
          }
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

    # Correctly access the content attribute
    return response.choices[0].message.content

# Example usage:
# prompt_text = "Please provide a detailed recipe for Koki Beans."
# recipe_description = generate_recipe_description(prompt_text)
# print(recipe_description)
