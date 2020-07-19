# Generated by Django 3.0.8 on 2020-07-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200710_1254'),
        ('posts', '0006_auto_20200711_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(default=31, on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
