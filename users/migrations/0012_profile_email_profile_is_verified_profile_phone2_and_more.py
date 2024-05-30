# Generated by Django 5.0.3 on 2024-05-28 01:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_student_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_verified",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone2",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.CreateModel(
            name="Teacher",
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
                ("is_active", models.BooleanField(default=True)),
                ("relation", models.CharField(max_length=128)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.school"
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
