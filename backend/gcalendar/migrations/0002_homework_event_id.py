# Generated by Django 5.0.7 on 2024-09-23 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcalendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
