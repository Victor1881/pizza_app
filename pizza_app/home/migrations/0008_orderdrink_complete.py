# Generated by Django 4.0.3 on 2022-04-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_orderd_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdrink',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]