# Generated by Django 4.1.3 on 2022-12-22 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_starred_boards'),
        ('workspaces', '0029_loguserrecentboards'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loguserrecentboards',
            old_name='user',
            new_name='profile',
        ),
        migrations.AlterUniqueTogether(
            name='loguserrecentboards',
            unique_together={('profile', 'board')},
        ),
    ]