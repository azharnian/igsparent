# Generated by Django 5.0.3 on 2024-03-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_frontoffice"),
    ]

    operations = [
        migrations.AddField(
            model_name="frontoffice",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]