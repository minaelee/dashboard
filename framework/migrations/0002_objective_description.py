# Generated by Django 5.1.5 on 2025-02-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("framework", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="objective",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
