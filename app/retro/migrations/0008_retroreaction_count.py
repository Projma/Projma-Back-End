# Generated by Django 4.1.3 on 2023-05-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0007_alter_retrosession_retro_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='retroreaction',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
