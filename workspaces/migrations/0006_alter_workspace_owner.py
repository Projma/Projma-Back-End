# Generated by Django 4.1.3 on 2022-11-22 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_birth_date'),
        ('workspaces', '0005_board_created_at_board_updated_at_file_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owning_workspaces', to='accounts.profile'),
        ),
    ]
