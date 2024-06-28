from django.core.management.base import BaseCommand
from ...models import Recipe  # Import your model here
import random


class Command(BaseCommand):
    help = 'Create random recipes'

    def handle(self, *args, **kwargs):
        for _ in range(10):  # Change the range to the number of dummy data you want to create
            Recipe.objects.create(
                title=f'Recipe {_}',
                instructions='Test instructions',
                nutritional_value=random.randint(100, 500),
                notes='Test notes',
                ethnicity='Test ethnicity',
                origin='Test origin'
            )
