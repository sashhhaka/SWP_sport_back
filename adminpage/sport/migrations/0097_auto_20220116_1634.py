# Generated by Django 3.1.8 on 2022-01-16 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0096_add_tablefunc_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.semester'),
        ),
    ]
