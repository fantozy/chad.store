# Generated by Django 5.1.5 on 2025-02-15 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="categoryimage",
            old_name="product",
            new_name="category",
        ),
    ]
