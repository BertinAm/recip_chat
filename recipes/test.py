from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import Recipe
from recipes.services import ChatGPTService


class RecipeTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch.object(ChatGPTService, 'generate_recipe')
    def test_generate_recipe(self, mock_generate_recipe):
        mock_generate_recipe.return_value = 'Test Recipe'
        response = self.client.get(reverse('generate-recipe'))
        self.assertEqual(response.status_code, 200)
        mock_generate_recipe.assert_called_once()

    def test_recipe_list(self):
        Recipe.objects.create(name='Recipe 1', field1='actual_value1',
                              field2='actual_value2')  # replace 'actual_value1' and 'actual_value2' with actual values
        response = self.client.get(reverse('recipe-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_recipe_detail(self):
        recipe1 = Recipe.objects.create(name='Recipe 1', field1='actual_value1',
                                        field2='actual_value2')  # replace 'actual_value1' and 'actual_value2' with actual values
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': recipe1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Recipe 1')