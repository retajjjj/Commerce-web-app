# Generated by Django 5.0.7 on 2024-08-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctions_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
