# Generated by Django 4.0.3 on 2022-04-15 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_completeorder_image_alter_completeorder_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinformation',
            name='order_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderinformation',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]