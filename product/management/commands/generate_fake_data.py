import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from product.models import Game,Category
from faker import Faker
from faker.providers import BaseProvider
from django.utils.text import slugify


class GameNameProvider(BaseProvider):
    def game_name(self):
        game_titles = [
            "Dota 2", "Assassin's Creed", "Super People",
            "Brawhalla", "Call of Duty", "WarFrame",
            "Apex Legends", "The Sims"
        ]
        return self.random_element(game_titles)

class Command(BaseCommand):
    help = 'Generate fake game data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(GameNameProvider)

        placeholder_images_path = "media/images/faker"
        image_files = os.listdir(placeholder_images_path)
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found in the database. Please add some categories first!'))
            return

        for _ in range(10):
            image_file_path = os.path.join(placeholder_images_path, fake.random_element(image_files))
            with open(image_file_path, "rb") as image_file:
                category = random.choice(categories)
                title = fake.game_name()
                slug = slugify(f"{title}-{fake.random_int(min=1, max=1000)}")
                game = Game.objects.create(
                    title=title,
                    summary=fake.text(),
                    slug=slug,
                    price=fake.random_int(min=1, max=60),
                    sold_count=fake.random_int(min=0, max=1000),
                    off=fake.random_int(min=0, max=100),
                    image=File(image_file),
                    category=category,
                )


                game.tags.add(*fake.words(nb=3))

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data!'))