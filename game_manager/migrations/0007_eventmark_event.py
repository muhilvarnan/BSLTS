# Generated by Django 2.2.6 on 2019-10-22 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0006_auto_20191022_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmark',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='game_manager.Event'),
        ),
    ]
