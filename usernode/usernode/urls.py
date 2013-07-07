from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
##################

from nodejs.views import index, login_view, logout_view, register_view, profile_view, edit_profile, tweet_, new_tweet

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    # url(r'^usernode/', include('usernode.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register_view, name="register"),
    url(r'^profile/(?P<email>.*)/$', profile_view, name="profile"),
    url(r'^edit/profile/(?P<email>.*)/$', edit_profile, name="edit_profile"),
    url(r'^tweet/$', tweet_, name="tweet"),
    url(r'^new-tweet/$', new_tweet, name="new_tweet"),

)
