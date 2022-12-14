# Generated by Django 4.1.3 on 2022-11-30 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_hotel_code_alter_hotel_name_alter_rate_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
