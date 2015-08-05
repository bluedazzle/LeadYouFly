# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0004_auto_20150805_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero1',
            field=models.ForeignKey(related_name='who_expert1', blank=True, to='LYFAdmin.Hero', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero2',
            field=models.ForeignKey(related_name='who_expert2', blank=True, to='LYFAdmin.Hero', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expert_hero3',
            field=models.ForeignKey(related_name='who_expert3', blank=True, to='LYFAdmin.Hero', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mentor',
            name='hero_list',
            field=models.ManyToManyField(related_name='who_uses', null=True, to='LYFAdmin.Hero', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.ForeignKey(related_name='comment_order', blank=True, to='LYFAdmin.Comment', null=True),
            preserve_default=True,
        ),
    ]
