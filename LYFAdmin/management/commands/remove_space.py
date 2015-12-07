# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from weichat.models import Channel

class Command(BaseCommand):
    def handle(self, *args, **options):
        channel_list = Channel.objects.all()
        for channel in channel_list:
            channel.phone = str(channel.phone).strip()
            channel.save()
        print 'mission complete'