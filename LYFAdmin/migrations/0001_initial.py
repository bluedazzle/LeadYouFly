# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('mark', models.FloatField(default=0.0)),
                ('content', models.CharField(default=b'', max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0.0)),
                ('course_info', models.CharField(default=b'', max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('hero_name', models.CharField(max_length=50)),
                ('hero_picture', models.CharField(default=b'', max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('account', models.CharField(unique=True, max_length=11)),
                ('nick', models.CharField(default=b'Mentor', max_length=20, null=True, blank=True)),
                ('status', models.IntegerField(default=1)),
                ('intro', models.CharField(default=b'', max_length=100)),
                ('good_at', models.IntegerField(default=1)),
                ('game_level', models.CharField(default=b'', max_length=8)),
                ('teach_area', models.CharField(default=b'', max_length=20)),
                ('qq', models.CharField(default=b'', max_length=20)),
                ('yy', models.CharField(default=b'', max_length=50)),
                ('phone', models.CharField(default=b'', max_length=11)),
                ('intro_detail', models.TextField(default=b'')),
                ('avatar', models.CharField(default=b'', max_length=200)),
                ('intro_video', models.CharField(default=b'', max_length=200)),
                ('expert_hero1', models.ForeignKey(related_name='who_expert1', to='LYFAdmin.Hero')),
                ('expert_hero2', models.ForeignKey(related_name='who_expert2', to='LYFAdmin.Hero')),
                ('expert_hero3', models.ForeignKey(related_name='who_expert3', to='LYFAdmin.Hero')),
                ('hero_list', models.ManyToManyField(related_name='who_uses', to='LYFAdmin.Hero')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoneyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(default=b'', max_length=8)),
                ('income', models.FloatField(default=0.0)),
                ('type', models.BooleanField(default=True)),
                ('info', models.CharField(default=b'', max_length=200)),
                ('belong', models.ForeignKey(related_name='men_money_records', to='LYFAdmin.Mentor')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('order_id', models.CharField(unique=True, max_length=22)),
                ('order_price', models.FloatField(default=0.0)),
                ('course_name', models.CharField(default=b'', max_length=50)),
                ('course_intro', models.CharField(default=b'', max_length=500)),
                ('learn_area', models.CharField(default=b'', max_length=30)),
                ('learn_type', models.IntegerField(default=1)),
                ('learn_hero', models.CharField(default=b'', max_length=20)),
                ('status', models.IntegerField(default=-1)),
                ('teach_video', models.CharField(default=b'', max_length=200)),
                ('if_upload_video', models.BooleanField(default=False)),
                ('teach_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('account', models.CharField(unique=True, max_length=11)),
                ('nick', models.CharField(default=b'Mentor', max_length=20, null=True, blank=True)),
                ('rank', models.IntegerField(default=1)),
                ('qq', models.CharField(default=b'', max_length=20)),
                ('yy', models.CharField(default=b'', max_length=50)),
                ('phone', models.CharField(default=b'', max_length=11)),
                ('avatar', models.CharField(default=b'', max_length=200)),
                ('follow', models.ManyToManyField(related_name='my_students', null=True, to='LYFAdmin.Mentor', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='belong',
            field=models.ForeignKey(related_name='stu_orders', to='LYFAdmin.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.ForeignKey(related_name='comment_order', to='LYFAdmin.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='teach_by',
            field=models.ForeignKey(related_name='men_orders', to='LYFAdmin.Mentor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='belong',
            field=models.ForeignKey(related_name='stu_messages', to='LYFAdmin.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='belong',
            field=models.ForeignKey(related_name='men_courses', to='LYFAdmin.Mentor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_by',
            field=models.ForeignKey(related_name='stu_comments', to='LYFAdmin.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_mentor',
            field=models.ForeignKey(related_name='men_comments', to='LYFAdmin.Mentor'),
            preserve_default=True,
        ),
    ]
