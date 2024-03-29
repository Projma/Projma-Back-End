# Generated by Django 4.1.3 on 2022-12-05 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_starred_boards'),
        ('workspaces', '0012_alter_task_doers_alter_task_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('reply_to', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='workspaces.comment')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.profile')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='workspaces.task')),
            ],
        ),
    ]
