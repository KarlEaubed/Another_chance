# Generated by Django 5.0.3 on 2024-05-12 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_postview'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostView',
        ),
    ]