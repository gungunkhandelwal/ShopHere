# Generated by Django 3.2.20 on 2024-01-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_details',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]