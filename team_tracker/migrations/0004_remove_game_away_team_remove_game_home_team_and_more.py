# Generated by Django 4.2.2 on 2023-07-04 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_tracker', '0003_rename_city_cflteam_location_cflteam_name_short_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='away_team',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_team',
        ),
        migrations.AddField(
            model_name='cflteam',
            name='abbreviation',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='game',
            name='api_game_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='game_number',
            field=models.IntegerField(default=0),
        ),
    ]
