from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class CustomUser(AbstractUser):
    image = ResizedImageField(size=[150, 150], crop=['middle', 'center'], quality=85, upload_to='images/profiles',null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(default='', null=True, blank=True)
    phone = models.CharField(default='', max_length=11, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(help_text="write a summary of the game story", null=True, blank=True)
    price = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    off = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games', null=True, blank=True)
    image = models.ImageField(upload_to="images/games")
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at', '-off'])]
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("game:game_detail", args=[self.id])

    def get_final_price(self):
        return self.price - ((self.price * self.off) // 100)





class Ticket(models.Model):
    class Status(models.TextChoices):
        LOGIN = 'Login & Logout Error', 'Login & Logout Error'
        BUY = 'Buying Error', 'Buying Error'
        OTHER = 'Other', 'Other'

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=Status.choices)
    message = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    buyer = models.ForeignKey(CustomUser, related_name="orders", on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{str(self.id)} : {self.game.title}"

    def cost(self):
        return self.game.get_final_price() * self.quantity
