# Generated by Django 4.1.3 on 2022-12-07 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0017_merge_20221207_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]