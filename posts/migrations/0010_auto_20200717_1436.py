# Generated by Django 3.0.8 on 2020-07-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_like_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
