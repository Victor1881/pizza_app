# Generated by Django 4.0.3 on 2022-04-15 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_remove_completeorder_user_completeorder_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completeorder',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='completeorder',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]