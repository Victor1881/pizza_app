# Generated by Django 4.0.3 on 2022-04-15 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_remove_completeorder_pizza_completeorder_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completeorder',
            name='order',
        ),
    ]
