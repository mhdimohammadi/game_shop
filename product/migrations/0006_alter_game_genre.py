# Generated by Django 5.1.6 on 2025-02-09 17:59

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_game_game_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ACTION', 'ACTION'), ('ADVENTURE', 'ADVENTURE'), ('FAMILY', 'FAMILY'), ('PUZZLE', 'PUZZLE'), ('SHOOTER', 'SHOOTER')], max_length=38),
        ),
    ]
