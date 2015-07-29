# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rec_mentor1', models.ForeignKey(related_name='ind_rec_1', blank=True, to='LYFAdmin.Mentor', null=True)),
                ('rec_mentor2', models.ForeignKey(related_name='ind_rec_2', blank=True, to='LYFAdmin.Mentor', null=True)),
                ('rec_mentor3', models.ForeignKey(related_name='ind_rec_3', blank=True, to='LYFAdmin.Mentor', null=True)),
                ('rec_mentor4', models.ForeignKey(related_name='ind_rec_4', blank=True, to='LYFAdmin.Mentor', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('qq', models.CharField(max_length=30, null=True, blank=True)),
                ('reported', models.CharField(max_length=30)),
                ('type', models.IntegerField(default=0)),
                ('content', models.CharField(default=b'', max_length=1000)),
                ('pic1', models.CharField(default=b'', max_length=200)),
                ('pic2', models.CharField(default=b'', max_length=200)),
                ('pic3', models.CharField(default=b'', max_length=200)),
                ('pic4', models.CharField(default=b'', max_length=200)),
                ('reporter', models.ForeignKey(related_name='stu_reports', to='LYFAdmin.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
