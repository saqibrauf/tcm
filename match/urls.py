
from django.urls import path
from . import views
from django.contrib.sitemaps import views as sm_views
from .sitemaps import MatchSitemap, SeriesSitemap

sitemaps = {
    'match': MatchSitemap(),
    #'series' : SeriesSitemap(),
}

urlpatterns = [
	#Sitemap
	path('sitemap.xml/', sm_views.index, {'sitemaps' : sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
	path('sitemap-<section>.xml/', sm_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #Website Views
    path('', views.index, name='index' ),
    path('<slug>/', views.match_detail, name='match_detail' ),
]