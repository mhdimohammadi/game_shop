from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images/user', blank=True,null=True)
    address = models.TextField(default='',null=True,blank=True)
    phone = models.CharField(default='',max_length=11,unique=True)





class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.TextField(help_text="write a summary of the game story", null=True, blank=True)
    price = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    off = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games',null=True, blank=True)
    image = models.ImageField(upload_to="images/games")
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at','-off'])]
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("game:game_detail", args=[self.id])

    def get_final_price(self):
        return self.price - ((self.price * self.off) // 100)


class Review(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    site = models.CharField(max_length=50, default="IGN")
    game = models.OneToOneField(Game, on_delete=models.PROTECT, related_name='review')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.author






class Ticket(models.Model):
    class Status(models.TextChoices):
        LOGIN = 'Login & Logout Error', 'Login & Logout Error'
        BUY = 'Buying Error', 'Buying Error'
        OTHER = 'Other', 'Other'

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50,choices=Status.choices)
    message = models.TextField()


    def __str__(self):
        return self.name