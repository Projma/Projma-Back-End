# Generated by Django 4.1.3 on 2022-12-06 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0013_attachment_delete_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='file_url',
            new_name='file',
        ),
    ]