"""lookmovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','websiteapp.views.login',name='login'),
    url(r'^sign/','websiteapp.views.sign',name='sign'),
    url(r'^exit/','websiteapp.views.exit',name='exit'),
    url(r'^$', 'websiteapp.views.index', name='index'),
    url(r'^search/cinema/by_district/','websiteapp.views.search_cinema_by_district',name='search_cinema_by_district'),
    url(r'^search/cinema/by_movie/','websiteapp.views.search_cinema_by_movie',name='search_cinema_by_movie'),
    url(r'^search/movie/total/','websiteapp.views.search_movie_total',name='search_movie_total'),
    url(r'^ticket/','websiteapp.views.ticket',name='ticket'),
    url(r'^create_db/','websiteapp.views.create_db',name='create_db'),
    url(r'^user_ticket_history/','websiteapp.views.user_ticket_history',name='user_ticket_history'),
    #url(r'^hottoday/', 'websiteapp.views.hottoday', name='hottoday'),
    url(r'^cinema/(\d+)', 'websiteapp.views.cinema', name='cinema'),
    url(r'^cinema_xml/(\d+)', 'websiteapp.views.cinema_xml', name='cinema_xml'),
    url(r'^hall/(\d+)/(\d\d\d\d-\d\d-\d\d)/(\d\d:\d\d:\d\d)', 'websiteapp.views.hall', name='hall'),
]