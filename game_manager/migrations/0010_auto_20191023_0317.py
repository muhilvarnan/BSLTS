# Generated by Django 2.2.6 on 2019-10-23 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0009_auto_20191022_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='group',
            field=models.CharField(choices=[('1', 'Group 1'), ('2', 'Group 2'), ('3', 'Group 3')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samithi',
            name='district',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='game_manager.District'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('B', 'Boy'), ('G', 'Girl')], default=None, max_length=1),
        ),
    ]
