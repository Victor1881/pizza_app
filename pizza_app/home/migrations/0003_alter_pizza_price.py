# Generated by Django 4.0.3 on 2022-04-09 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_pizza_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='price',
            field=models.CharField(default=13, max_length=30),
        ),
    ]
