# Generated by Django 5.1.6 on 2025-06-03 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0012_alter_classfeature_scope'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ability', models.CharField(help_text='e.g., DEX, INT', max_length=3)),
                ('is_advanced', models.BooleanField(default=False, help_text="Advanced skills can't be increased normally.")),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('damage', models.CharField(help_text='e.g., 1d8 Piercing', max_length=50)),
                ('category', models.CharField(choices=[('simple', 'Simple'), ('martial', 'Martial'), ('special', 'Special')], max_length=10)),
                ('is_melee', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeaponTrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('requires_value', models.BooleanField(default=False, help_text='e.g., Brutal D8/D10 etc.')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponTraitValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, help_text='Only used if trait.requires_value=True', max_length=50, null=True)),
                ('trait', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.weapontrait')),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.weapon')),
            ],
            options={
                'unique_together': {('weapon', 'trait')},
            },
        ),
        migrations.AddField(
            model_name='weapon',
            name='traits',
            field=models.ManyToManyField(blank=True, through='characters.WeaponTraitValue', to='characters.weapontrait'),
        ),
        migrations.CreateModel(
            name='CharacterSubSkillProficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subskill_proficiencies', to='characters.character')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.proficiencylevel')),
                ('subskill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.subskill')),
            ],
            options={
                'unique_together': {('character', 'subskill')},
            },
        ),
        migrations.CreateModel(
            name='CharacterSkillRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_points', models.IntegerField(default=0, help_text='Allocated from ability score increases, NOT proficiency.')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_ratings', to='characters.character')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.skill')),
            ],
            options={
                'unique_together': {('character', 'skill')},
            },
        ),
    ]
