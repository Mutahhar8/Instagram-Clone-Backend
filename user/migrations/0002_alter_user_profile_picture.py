# Generated by Django 4.2 on 2023-05-11 08:09

from django.db import migrations, models
import storages.backends.gcloud


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.gcloud.GoogleCloudStorage(), upload_to='profile_pictures'),
        ),
    ]
