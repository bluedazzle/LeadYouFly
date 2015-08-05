# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LYFAdmin', '0010_mentor_freeae'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentor',
            old_name='freeae',
            new_name='freeze',
        ),
    ]
