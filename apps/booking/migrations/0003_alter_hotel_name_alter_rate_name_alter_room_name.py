# Generated by Django 4.1.3 on 2022-11-30 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_inventory_date_alter_rate_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]