# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from weichat.models import Promotion, Channel


class Command(BaseCommand):
    def handle(self, *args, **options):
        message_list = Promotion.objects.all()
        for message in message_list:
            message.delete()

        message_list = Channel.objects.all()
        for message in message_list:
            message.delete()
        print 'message delete complete!'
