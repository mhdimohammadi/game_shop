import os
from django.core.management.base import BaseCommand
from django.core.files import File
from product.models import Game
from faker import Faker
from faker.providers import BaseProvider

class GameNameProvider(BaseProvider):
    def game_name(self):
        game_titles = [
            "Dota 2", "Assassin's Creed", "Super People",
            "Brawhalla", "Call of Duty", "WarFrame",
            "Apex Legends","The Sims"
        ]
        return self.random_element(game_titles)

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(GameNameProvider)

        placeholder_images_path = "../../../media/images/faker"  # Directory containing placeholder images
        image_files = os.listdir(placeholder_images_path)  # List of files in the directory

        for _ in range(15):  # Generate 15 fake entries
            image_file_path = os.path.join(placeholder_images_path, fake.random_element(image_files))
            with open(image_file_path, "rb") as image_file:
                Game.objects.create(
                    title=fake.game_name(),
                    description=fake.text(max_nb_chars=100),
                    summary=fake.text(),
                    price=fake.random_int(min=1, max=60),
                    sold_count=fake.random_int(min=0, max=1000),
                    off=fake.random_int(min=0, max=100),
                    tags=fake.word(),
                    image=File(image_file),
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data!'))