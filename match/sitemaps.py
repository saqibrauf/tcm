from django.contrib.sitemaps import Sitemap
from .models import Match, Series, Tag

class MatchSitemap(Sitemap):    
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Match.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
        

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
        return Tag.objects.all()