# Generated by Django 4.1.3 on 2023-04-14 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_rename_voter_pollanswer_voters_poll_is_known'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='board',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='board.board'),
            preserve_default=False,
        ),
    ]
