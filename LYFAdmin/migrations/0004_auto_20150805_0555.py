# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0003_mentor_id_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='hero_picture',
            field=models.CharField(default=b' ', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='avatar',
            field=models.CharField(default=b' ', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero1',
            field=models.ForeignKey(related_name='who_expert1', default=None, to='LYFAdmin.Hero'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero2',
            field=models.ForeignKey(related_name='who_expert2', default=None, to='LYFAdmin.Hero'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero3',
            field=models.ForeignKey(related_name='who_expert3', default=None, to='LYFAdmin.Hero'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='game_level',
            field=models.CharField(default=b' ', max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='hero_list',
            field=models.ManyToManyField(default=None, related_name='who_uses', to='LYFAdmin.Hero'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='id_picture',
            field=models.CharField(default=b' ', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='intro',
            field=models.CharField(default=b' ', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='intro_detail',
            field=models.TextField(default=b' '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='intro_video',
            field=models.CharField(default=b' ', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='phone',
            field=models.CharField(default=b' ', max_length=11),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='qq',
            field=models.CharField(default=b' ', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='teach_area',
            field=models.CharField(default=b' ', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='yy',
            field=models.CharField(default=b' ', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.CharField(default=b' ', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(default=b' ', max_length=11),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='qq',
            field=models.CharField(default=b' ', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='yy',
            field=models.CharField(default=b' ', max_length=50),
            preserve_default=True,
        ),
    ]
