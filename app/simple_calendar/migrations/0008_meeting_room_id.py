# Generated by Django 4.1.3 on 2023-04-19 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_calendar', '0007_alter_meeting_end_alter_meeting_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='room_id',
            field=models.IntegerField(null=True),
        ),
    ]
