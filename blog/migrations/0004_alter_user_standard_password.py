# Generated by Django 4.2.7 on 2024-04-11 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_user_standard_nom_user_standard_prenom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_standard',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]