from django.contrib.sitemaps import Sitemap
from .models import Match, Series, Tag

#This is a sample sitemap generator for my new website
"""
class MatchSitemap(Sitemap):   

    def items(self):
        matches=Match.objects.all()
        urls = list()
        for m in matches:
            tags=m.tags.all()
            for t in tags:                
                url = '/' + t.slug + '/' + m.slug
                urls.append(url)
        return urls

    changefreq = "hourly"
    priority = 1.0

    def location(self, item):
        return item
"""     

class SeriesSitemap(Sitemap):    
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Series.objects.all()

    def lastmod(self, obj):
        return obj.date

class TagSitemap(Sitemap):    
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Tag.objects.all().order_by('tag_name')

class CompleteMatches(Sitemap):    
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Match.objects.all()

    def lastmod(self, obj):
        return obj.updated_at