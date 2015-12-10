# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from weichat.models import Question

class Command(BaseCommand):
    def handle(self, *args, **options):
        for question in Question.objects.all():
            if '1006' in question.answer:
                question.answer = unicode(question.answer).replace('1006', '小飞')
                question.save()
        print 'mission complete!'