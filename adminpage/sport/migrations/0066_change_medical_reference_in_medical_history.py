# Generated by Django 3.1.8 on 2021-08-02 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0065_medicalgrouphistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalgrouphistory',
            name='medical_group_reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sport.medicalgroupreference'),
        ),
    ]
