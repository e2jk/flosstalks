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
import django.views.generic as generic_views
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from flosstalks_app.models import Project, Series
import json

def get_search_values(request):
    #TODO: Keep these values in cache for performance reasons
    search_values = []
    for p in Project.objects.exclude(status="HD").exclude(status="NW"):
        nice_url = "/%s" % p.nice_url if p.nice_url else \
                   reverse('project', args=[p.pk])
        search_values.append({"value": p.name, "url": nice_url})
    for s in Series.objects.all():
        nice_url = "/%s" % s.nice_url if s.nice_url else \
                   reverse('series', args=[s.pk])
        search_values.append({"value": s.name, "url": nice_url})
    json_response = json.dumps(sorted(search_values))
    return HttpResponse(json_response, mimetype='application/json')


class TemplateView(generic_views.TemplateView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]

        if "index.html" == self.template_name:
            # Highlight 3 projects on the home page
            context['highlighted_projects'] = Project.objects\
                                                .exclude(status="HD")\
                                                .exclude(status="NW")\
                                                .order_by('?')[:3]

        return context

class ListView(generic_views.ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]

        if "projects_list.html" == self.template_name:
            # Calculate when to start the new column
            context['new_column_index'] = ((len(context['projects_list']) + 1) / 2)

        return context

class DetailView(generic_views.DetailView):
    def get(self, request, **kwargs):
        orig = super(DetailView, self).get(request, **kwargs)

        if self.template_name in ("project_detail.html", "series_detail.html"):
            # Redirect to this project's nice url if it's defined
            if self.object.nice_url:
                return HttpResponsePermanentRedirect("/%s" % self.object.nice_url)

        return orig

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]

        if "resource_detail.html" == self.template_name:
            # List all the active projects associated with this resource
            context['active_projects'] = context['resource'].projects.exclude(status="HD")

        return context

def search(request):
    search_term = request.GET.get("q")
    projects = Project.objects.filter(name__icontains=search_term) if \
                        search_term else None
    series = Series.objects.filter(name__icontains=search_term) if \
                        search_term else None
    c = RequestContext(request, {
        'search_term': search_term,
        'projects': projects,
        'series': series,
    })
    return render_to_response('search.html', c)

def nice_url(request, requested_value):
    # The nice url is stored in urlquote-encoded form, so make sure that
    # this is what gets used to search.
    # Example: commas are stored as %2C in the database, but are provided
    # as , in requested_value.
    requested_value = urlquote(requested_value)
    try:
        # Nice url of a project?
        project = Project.objects.get(nice_url=requested_value)
        c = RequestContext(request, {
            'project': project,
        })
        return render_to_response('project_detail.html', c)
    except Project.DoesNotExist:
        try:
            # Nice url of a series?
            series = Series.objects.get(nice_url=requested_value)
            c = RequestContext(request, {
                'series': series,
            })
            return render_to_response('series_detail.html', c)
        except Series.DoesNotExist:
            # Not a valid nice url
            #TODO: This breaks Django's automatic redirect from /r/22 to /r/22/
            raise Http404
