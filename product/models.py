from django.db import models

class Game(models.Model):
    class Genre(models.TextChoices):
        ACTION = 'ACTION', 'ACTION'
        ADVENTURE = 'ADVENTURE', 'ADVENTURE'
        FAMILY = 'FAMILY', 'FAMILY'
        PUZZLE = 'PUZZLE', 'PUZZLE'
        SHOOTER = 'SHOOTER', 'SHOOTER'

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    game_id = models.CharField(max_length=20,unique=True)
    genre = models.CharField(max_length=20,choices=Genre.choices)
    image = models.ImageField(upload_to="images/games")


