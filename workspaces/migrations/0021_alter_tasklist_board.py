# Generated by Django 4.1.3 on 2022-12-08 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0020_label_board_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasklists', to='workspaces.board'),
        ),
    ]