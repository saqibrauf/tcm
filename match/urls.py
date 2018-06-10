
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('predictions/<slug>/', views.match_detail, name='match_detail' ),
]


#Sitemap

from .sitemaps import MatchSitemap, SeriesSitemap

sitemaps = {
    'match': MatchSitemap(),
    #'series' : SeriesSitemap(),
}

from django.contrib.sitemaps import views

urlpatterns += [
    path('sitemap.xml/', views.index, {'sitemaps' : sitemaps }),
    path('sitemap-<section>.xml/', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

