# Generated by Django 3.1.8 on 2023-06-28 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ach_admin', '0010_auto_20230629_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='icon',
            field=models.ImageField(upload_to='achievements'),
        ),
    ]
