from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView, ListView
from flosstalks_app.models import Project

urlpatterns = patterns('',
#    url(r'^$',
#        ListView.as_view(
#            queryset=Poll.objects.order_by('-pub_date')[:5],
#            context_object_name='latest_poll_list',
#            template_name='polls/index.html')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^p/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Project,
            template_name='project_detail.html')),
#    url(r'^(?P<pk>\d+)/results/$',
#        DetailView.as_view(
#            model=Poll,
#            template_name='polls/results.html'),
#        name='poll_results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
