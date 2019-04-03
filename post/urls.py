from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'welcome'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^myProfile/(\d+)', views.myProfile, name='myProfile'),
    url(r'^project/', views.project, name='project'),
    url(r'^images/(\d+)',views.images,name ='images'),
    url(r'^comments/(\d+)',views.comments,name="comments"),
    url(r'^votes/(\d+)',views.votes,name="votes"),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^api/merch/$', views.ProfileList.as_view()),
    url(r'^api/project/$', views.ProjectList.as_view())
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)