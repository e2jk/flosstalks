#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is part of FLOSS Talks.
#
#    FLOSS Talks is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FLOSS Talks is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with FLOSS Talks.  If not, see <http://www.gnu.org/licenses/>.
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from flosstalks_app.models import Project, Series, Resource
from flosstalks_app.views import TemplateView, ListView, DetailView

urlpatterns = patterns('',
    url(r'^$',
        cache_page(300)(# Cache the home page only for 5 minutes
            TemplateView.as_view(template_name='index.html')
        ),
        name='home'),
    url(r'^projects$',
        ListView.as_view(
            queryset=Project.objects.exclude(status="HD")\
                                    .exclude(status="NW")\
                                    .order_by('name'),
            paginate_by=20,
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
    url(r'^p/(?P<pk>\d+)/add-resource$',
        'flosstalks_app.views.project_add_resource',
        name='project_add_resource'),
    url(r'^p/(?P<pk>\d+)/resource-added$',
        DetailView.as_view(
            model=Project,
            template_name='project_resource_added.html'),
        name='project_resource_added'),
    url(r'^s/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Series,
            template_name='series_detail.html'),
        name='series'),
    url(r'^r/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Resource,
            template_name='resource_detail.html'),
        name='resource'),
    url(r'^search$', 'flosstalks_app.views.search'),
    url(r'^search-values.json$', 'flosstalks_app.views.get_search_values'),
    url(r'^(?P<requested_value>.+)$', 'flosstalks_app.views.nice_url'),
)
