# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from LYFAdmin.models import Mentor

class Command(BaseCommand):
    def handle(self, *args, **options):
        mentor_list = Mentor.objects.all()
        for mentor in mentor_list:
            mentor.iden_income = 0
            mentor.save()
        print 'identify money reset complete!'