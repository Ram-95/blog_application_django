# Generated by Django 3.0.8 on 2020-12-29 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20201229_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='posts_images'),
        ),
    ]
