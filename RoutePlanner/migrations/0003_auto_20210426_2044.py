# Generated by Django 3.2 on 2021-04-26 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoutePlanner', '0002_auto_20210326_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='image',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='route',
            name='length',
            field=models.FloatField(default=0.0),
        ),
    ]
