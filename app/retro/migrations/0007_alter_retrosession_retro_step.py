# Generated by Django 4.1.3 on 2023-05-11 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0006_alter_retrosession_retro_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retrosession',
            name='retro_step',
            field=models.SmallIntegerField(default=0),
        ),
    ]
