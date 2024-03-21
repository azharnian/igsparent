# Generated by Django 5.0.3 on 2024-03-20 02:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_frontoffice_is_active"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="frontoffice",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="frontoffice_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
