# Generated by Django 3.1.1 on 2020-11-24 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20201123_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create',
            name='Description',
            field=models.TextField(max_length=300),
        ),
    ]