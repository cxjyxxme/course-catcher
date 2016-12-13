"""CourseCatcher URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from CourseCatcher.view import *
from django.conf import settings

urlpatterns = [
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                            { 'document_root':settings.STATIC_ROOT }),
	url(r'^add_user/$', add_user),
	url(r'^deal_add_user/$', deal_add_user),
    url(r'^add_code/$', add_code),
    url(r'^deal_add_code/$', deal_add_code),
    url(r'^$', index),
    url(r'^deal_login/$', deal_login),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^user_info/$', user_info),
    url(r'^add_task/$', add_task),
	url(r'^add_courses/$', user_info),
	url(r'^remove_course/$', remove_course),
	url(r'^test/$', test),
]
