# Generated by Django 5.0.7 on 2024-08-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctions_bids_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='category',
            field=models.CharField(max_length=64),
        ),
    ]
