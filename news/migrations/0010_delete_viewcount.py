# Generated by Django 4.0.1 on 2022-02-17 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_viewcount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ViewCount',
        ),
    ]
