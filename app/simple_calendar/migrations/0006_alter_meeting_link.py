# Generated by Django 4.1.3 on 2023-04-17 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_calendar', '0005_meeting_calendar_meeting_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='link',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]