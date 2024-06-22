# Generated by Django 5.0 on 2024-05-28 12:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("France", "France"),
                            ("Belgium", "Belgium"),
                            ("UK", "UK"),
                            ("Spain", "Spain"),
                            ("Germany", "Germany"),
                            ("Italy", "Italy"),
                            ("Greece", "Greece"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("PS4/PS5", "PS4/PS5"),
                            ("XBOX", "XBOX"),
                            ("PC", "PC"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "rank",
                    models.CharField(
                        choices=[
                            ("Bronze", "Bronze"),
                            ("Silver", "Silver"),
                            ("Gold", "Gold"),
                            ("Platinum", "Platinum"),
                            ("Diamond", "Diamond"),
                            ("Master", "Master"),
                            ("Predator", "Predator"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]