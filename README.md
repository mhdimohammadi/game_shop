LUGX game shop
This is an e_commerce web application developed by django. in this project I used ajax for sections like switching category 
in games list and cart actions. I used sessions for developing the cart and redis as session engine for improved performance.
I also use redis for caching some data in the game detail template. for the authentications I used tokens for better and more
secure authentication.
________________________________________________________________________________________________________________________________
SETUP:
for installing requirements use pip install -r requirements.txt in the terminal.
if you are cloning the project from GitHub you should make a .env file and define it like the .env.example file.
for generating fake categories use python manage.py generate_fake_category in the terminal
for generating fake games use python manage.py generate_fake_data in the terminal. please use the above command first so the categories are generated for games.
install redis.
[use Docker for easier setup, you can pull the image from my game_shop repo in https://hub.docker.com/repositories/evilmm]
________________________________________________________________________________________________________________________________
Additional description:
The original templates which I downloaded from Google didn't have the profile and order templates, so I created them my self
with the help of the AI that's why they are a little bit janky.
If you want to customize the project and then use docker to build an image you should do two things in settings.py :
1. add 'HOST': config('DATABASE_HOST', 'db'), in the databases in the default dict.
2. change the 'redis://localhost:6379/1' in the CACHES into 'redis://redis:6379/1'.