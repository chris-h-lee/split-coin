# Generated by Django 3.1.1 on 2020-11-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20201122_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create',
            name='Description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='create',
            name='Event',
            field=models.TextField(max_length=10),
        ),
    ]
