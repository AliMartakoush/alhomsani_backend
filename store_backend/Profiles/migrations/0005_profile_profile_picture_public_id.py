# Generated by Django 5.1.1 on 2025-04-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0004_rename_profile_picture_profile_profile_picture_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture_public_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
