# Generated by Django 5.0.6 on 2024-06-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0005_profile_last_activity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="last_activity",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
