from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['stackbase:home']

    def location(self, item):
        return reverse(item)

from stackbase.models import Question
 
 
class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Question.objects.all()

    def lastmod(self, obj):
        return obj.date_created
        
    def location(self,obj):
        return '/questions/%s' % (obj.pk)