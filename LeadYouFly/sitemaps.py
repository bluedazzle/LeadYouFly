# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from LYFAdmin.models import Notice, Mentor

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Notice.objects.all()

    def lastmod(self, item):
        return item.create_time

    def location(self, item):
        return r'/notice_detail?id={0}'.format(item.id)


class MentorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Mentor.objects.filter(disabled=False)

    def lastmod(self, item):
        return item.modify_time

    def location(self, item):
        return r'/mentor_detail?mentor_id={0}'.format(item.id)


class SearchPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return ['search']

    def location(self, item):
        return r'/search_teacher'


class IndexPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['index']

    def location(self, item):
        return r''


class StaticPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['about_us', 'contact_us', 'become_mentor', 'laws', 'problems', 'service']

    def location(self, item):
        return reverse(item)