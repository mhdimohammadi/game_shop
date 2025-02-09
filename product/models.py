from django.db import models
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField




class Game(models.Model):
    class Genre(models.TextChoices):
        ACTION = 'ACTION', 'ACTION'
        ADVENTURE = 'ADVENTURE', 'ADVENTURE'
        FAMILY = 'FAMILY', 'FAMILY'
        PUZZLE = 'PUZZLE', 'PUZZLE'
        SHOOTER = 'SHOOTER', 'SHOOTER'

    title = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.TextField(help_text="write a summary of the game story",null=True, blank=True)
    price = models.IntegerField(default=0)
    genre = MultiSelectField(choices=Genre.choices)
    image = models.ImageField(upload_to="images/games")
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]
        verbose_name = 'Game'
        verbose_name_plural = 'Games'


    def __str__(self):
        return self.title



