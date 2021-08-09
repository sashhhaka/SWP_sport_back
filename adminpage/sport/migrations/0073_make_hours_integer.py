# Generated by Django 3.1.8 on 2021-08-08 12:59

from django.db import migrations, models
import sport.models.attendance


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0072_auto_20210808_1618'),
    ]

    operations = [
        migrations.RunSQL('UPDATE attendance SET hours = CEIL(hours)'),
        migrations.AlterField(
            model_name='attendance',
            name='hours',
            field=models.IntegerField(default=1, validators=[sport.models.attendance.validate_hours]),
        ),

        migrations.RunSQL('UPDATE reference SET hours = CEIL(hours)'),
        migrations.AlterField(
            model_name='reference',
            name='hours',
            field=models.IntegerField(default=0),
        ),

        migrations.RunSQL('UPDATE self_sport_report SET hours = CEIL(hours)'),
        migrations.AlterField(
            model_name='selfsportreport',
            name='hours',
            field=models.IntegerField(default=0),
        ),
    ]
