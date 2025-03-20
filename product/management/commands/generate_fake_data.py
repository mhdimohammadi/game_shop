from django.core.management.base import BaseCommand
from product.models import Game
from faker import Faker

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(15):  # Generate 100 fake entries
            Game.objects.create(
                title=fake.name(),
                description=fake.text(max_nb_chars=100),
                summary=fake.text(),
                price=fake.random_int(min=1,max=60),
                sold_count=fake.random_int(),
                off=fake.random_int(min=0,max=100),
                tags=fake.word(),
                image=fake.image_url(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data!'))
