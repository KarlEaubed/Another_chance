# Generated by Django 4.2.7 on 2024-03-21 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitewebpam', '0003_remove_info_utilisateurs_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitewebpam',
            name='stockage',
            field=models.CharField(max_length=150, null=True),
        ),
    ]