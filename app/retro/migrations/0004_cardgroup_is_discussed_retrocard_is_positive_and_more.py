# Generated by Django 4.1.3 on 2023-05-11 13:17

from django.db import migrations, models
import django.db.models.deletion
import retro.types


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_starred_boards'),
        ('retro', '0003_alter_retrocard_card_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardgroup',
            name='is_discussed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='retrocard',
            name='is_positive',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='retroreaction',
            name='reactor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='retro_reactions', to='accounts.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='retrosession',
            name='retro_step',
            field=models.SmallIntegerField(default=retro.types.RetroSteps['ICEBREAKER']),
        ),
        migrations.AddField(
            model_name='retrosession',
            name='vote_limitation',
            field=models.IntegerField(default=-1, help_text='the default is -1 which means no limitation'),
        ),
        migrations.AlterUniqueTogether(
            name='retroreaction',
            unique_together={('card_group', 'reactor')},
        ),
        migrations.RemoveField(
            model_name='retroreaction',
            name='type',
        ),
    ]
