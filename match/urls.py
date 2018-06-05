from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index' ),
    re_path('^predictions/(?P<slug>[-\w]+)/$', views.match_detail, name='match_detail' ),
    #re_path('^(?P<t_slug>[-\w]+)/predictions/(?P<slug>[-\w]+)$', views.detail, name='detail' ),
]