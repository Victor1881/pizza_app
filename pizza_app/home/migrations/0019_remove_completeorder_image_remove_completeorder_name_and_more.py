# Generated by Django 4.0.3 on 2022-04-15 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_orderinformation_order_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completeorder',
            name='image',
        ),
        migrations.RemoveField(
            model_name='completeorder',
            name='name',
        ),
        migrations.RemoveField(
            model_name='completeorder',
            name='price',
        ),
        migrations.RemoveField(
            model_name='completeorder',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='completeorder',
            name='total',
        ),
    ]
