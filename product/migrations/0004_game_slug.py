# Generated by Django 5.1.6 on 2025-02-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_game_options_game_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
