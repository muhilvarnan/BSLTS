# Generated by Django 2.2.6 on 2019-11-06 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0023_auto_20191106_0209'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ParticipantsFamily',
            new_name='ParticipantFamily',
        ),
    ]