# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from LYFAdmin.models import Mentor

class Command(BaseCommand):
    def handle(self, *args, **options):
        account = args[0]
        mentor = Mentor.objects.get(account=account)
        comment_list = mentor.get_comment_list()
        for comment in comment_list:
            comment.mark = 5.0
            comment.save()
        print 'comment mark modify success'