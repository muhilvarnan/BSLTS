# Generated by Django 2.2.6 on 2019-10-27 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0017_auto_20191024_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='participants',
            field=models.ManyToManyField(blank=True, to='game_manager.Participant'),
        ),
    ]
