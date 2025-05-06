from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Game
from django.core.cache import cache


@receiver([post_save,post_delete],sender=Game)
def invalidate_game_cache(sender,instance,**kwargs):
    cache.delete_pattern('*game_list*')