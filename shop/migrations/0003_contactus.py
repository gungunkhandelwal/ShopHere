# Generated by Django 3.2.20 on 2024-01-22 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_details_digital'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(default='', max_length=70)),
                ('desc', models.TextField()),
            ],
        ),
    ]
