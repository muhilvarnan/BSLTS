# Generated by Django 2.2.6 on 2019-10-28 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0018_auto_20191027_1633'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventMark',
        ),
        migrations.DeleteModel(
            name='Judge',
        ),
    ]