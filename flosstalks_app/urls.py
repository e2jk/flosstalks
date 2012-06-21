from django.conf.urls import patterns, include, url
from django.views.generic import DetailView
from flosstalks_app.models import Project, Series
from flosstalks_app.views import TemplateView, ListView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^projects$',
        ListView.as_view(
            model=Project,
            context_object_name='projects_list',
            template_name='projects_list.html'),
        name='projects'),
    url(r'^series$',
        ListView.as_view(
            model=Series,
            context_object_name='series_list',
            template_name='series_list.html'),
        name='series_list'),
    url(r'^about$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^p/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Project,
            template_name='project_detail.html'),
        name='project'),
    url(r'^s/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Series,
            template_name='series_detail.html'),
        name='series'),
#    url(r'^(?P<pk>\d+)/results/$',
#        DetailView.as_view(
#            model=Poll,
#            template_name='polls/results.html'),
#        name='poll_results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
