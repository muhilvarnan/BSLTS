# Generated by Django 2.2.6 on 2019-10-24 02:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('game_manager', '0013_auto_20191023_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('max_age_limit', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_manager.Group'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_manager.Group'),
        ),
    ]
