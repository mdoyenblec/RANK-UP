# Generated by Django 5.0.6 on 2024-05-30 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_profile_gaming_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to="thumbnails/"),
        ),
    ]
