# Generated by Django 5.0.7 on 2024-08-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
