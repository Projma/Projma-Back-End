# Generated by Django 4.1.3 on 2023-05-06 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0006_poll_creator'),
        ('accounts', '0008_alter_profile_starred_boards'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='RetroSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrating_retro_sessions', to='accounts.profile')),
                ('attendees', models.ManyToManyField(related_name='retro_sessions', to='accounts.profile')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retro_sessions', to='board.board')),
            ],
        ),
        migrations.CreateModel(
            name='RetroReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=7)),
                ('card_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retro_reactions', to='retro.cardgroup')),
            ],
        ),
        migrations.CreateModel(
            name='RetroCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('card_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retro_cards', to='retro.cardgroup')),
            ],
        ),
        migrations.AddField(
            model_name='cardgroup',
            name='retro_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_groups', to='retro.retrosession'),
        ),
    ]
