# Generated by Django 3.0.4 on 2020-03-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
