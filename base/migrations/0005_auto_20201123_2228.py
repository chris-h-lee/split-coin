# Generated by Django 3.1.1 on 2020-11-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20201123_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create',
            name='duration',
            field=models.TextField(blank=True, null=True),
        ),
    ]
