from django.conf.urls import patterns, url
#import relavant django machinery that we use to create URL mappings
#provice us with access to our simple view 
from rango import views

#use a tuple, must be called urlpatterns,contains a series of calls to the url()
#only one mapping here
#1st parameter is regular expression ^$
#2nd parameter is the view invoked 
#3rd parameter is optional, for differentiate 
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        #url(r'^search/$', views.search, name="search"),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^goto/$', views.track_url, name='track_url'),
        url(r'^like_category/$', views.like_category, name='like_category'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        )
