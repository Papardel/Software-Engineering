# Generated by Django 5.0.3 on 2024-03-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csv',
            name='data',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='image',
            name='data',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='json',
            name='data',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='text',
            name='data',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='data',
            field=models.BinaryField(),
        ),
    ]
