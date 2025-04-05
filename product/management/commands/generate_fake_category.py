from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from faker.providers import BaseProvider

from product.models import Category


class CategoryNameProvider(BaseProvider):
    def category_name(self):
        category_titles = [
            "Action", "Adventure", "RPG", "Platformer",
            "Family", "Shooter", "Puzzle",
        ]
        return self.random_element(category_titles)




class Command(BaseCommand):
    help = 'Generate fake game-related category data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(CategoryNameProvider)
        for _ in range(7):
            name = fake.category_name()
            slug = slugify(f"{name}-{fake.random_int(min=1, max=1000)}")


            Category.objects.create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS(f'Created category: {name}, slug: {slug}'))