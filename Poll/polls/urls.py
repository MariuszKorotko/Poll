from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import DetailView, ResultsView, vote

app_name = 'polls'
urlpatterns = [
    url(r'^$', auth_views.login,
        {'template_name': 'polls/index.html'},
    name='index-login'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', vote, name='vote'),
]