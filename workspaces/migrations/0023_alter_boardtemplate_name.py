# Generated by Django 4.1.3 on 2022-12-08 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0022_alter_label_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardtemplate',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]