
from django.urls import path, re_path
from . import views
from django.contrib.sitemaps import views as sm_views
from .sitemaps import MatchSitemap, SeriesSitemap, TagSitemap

sitemaps = {
    'match': MatchSitemap(),
    'series' : SeriesSitemap(),
    'tag' : TagSitemap(),
}

urlpatterns = [

	#Sitemap
	path('sitemap.xml/', sm_views.index, {'sitemaps' : sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
	path('sitemap-<section>.xml/', sm_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    #Website Views
    path('', views.index, name='index' ),    
    path('upcoming-matches/', views.upcoming_matches, name='upcoming_matches'),
    path('predictions/<slug>/', views.match_detail, name='match_detail' ),
    path('series/<slug>/', views.series_detail, name='series_detail' ),
    path('tag/<slug>/', views.tag_detail, name='tag_detail' ),

    #scorecard
    path('scorecard/', views.scorecard, name='scorecard' ),

]