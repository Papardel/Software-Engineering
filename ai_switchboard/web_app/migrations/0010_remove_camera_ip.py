# Generated by Django 5.0.3 on 2024-05-11 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0009_camera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='ip',
        ),
    ]
