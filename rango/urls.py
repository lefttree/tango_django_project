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
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),)
