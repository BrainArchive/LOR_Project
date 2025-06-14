# Generated by Django 5.1.6 on 2025-05-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0009_alter_subclasstierlevel_subclass_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classfeature',
            name='mastery_rank',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Rank 0'), (1, 'Rank 1'), (2, 'Rank 2'), (3, 'Rank 3'), (4, 'Rank 4')], help_text='(Only for modular_mastery subclass_feat) Mastery Rank (0…4).', null=True),
        ),
        migrations.AddField(
            model_name='classfeature',
            name='tier',
            field=models.PositiveIntegerField(blank=True, help_text='(Only for modular_linear subclass_feat) Tier index (1, 2, 3, …).', null=True),
        ),
        migrations.AlterField(
            model_name='classfeature',
            name='min_level',
            field=models.PositiveIntegerField(blank=True, help_text='(Optional) extra minimum class-level required to pick this feature, beyond tier mapping.', null=True),
        ),
        migrations.AlterField(
            model_name='subclasstierlevel',
            name='tier',
            field=models.PositiveIntegerField(help_text='Tier index (e.g. 1, 2, 3, …). Must match the integer suffix on feature.code.'),
        ),
        migrations.AlterField(
            model_name='subclasstierlevel',
            name='unlock_level',
            field=models.PositiveIntegerField(help_text='Class-level at which this tier becomes available.', null=True),
        ),
    ]
