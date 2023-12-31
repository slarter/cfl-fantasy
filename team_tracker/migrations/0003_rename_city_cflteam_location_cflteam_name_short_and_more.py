# Generated by Django 4.2.2 on 2023-06-30 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_tracker', '0002_alter_gamestatlog_value_alter_stat_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cflteam',
            old_name='city',
            new_name='location',
        ),
        migrations.AddField(
            model_name='cflteam',
            name='name_short',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='teamfantasyteam',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
