# Generated by Django 3.1.6 on 2021-03-23 06:21

import celebda.models
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('celebda', '0002_account_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(upload_to=celebda.models.account_image_path),
        ),
    ]
