# Generated by Django 4.0.3 on 2022-04-15 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_remove_completeorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completeorder',
            name='user',
        ),
        migrations.AddField(
            model_name='completeorder',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.orderinformation'),
        ),
    ]
