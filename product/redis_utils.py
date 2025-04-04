import redis
import json


redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=1,
)


def cache_game_details(game_id, game_data):
    redis_client.set(f'game:{game_id}', json.dumps(game_data), ex=3600)  # Cache for 1 hour (3600 seconds)


def get_cached_game_details(game_id):
    cached_data = redis_client.get(f'game:{game_id}')
    if cached_data:
        return json.loads(cached_data)
    return None


def clear_game_cache(game_id):
    redis_client.delete(f'game:{game_id}')
