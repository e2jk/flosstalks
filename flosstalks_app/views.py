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
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from flosstalks_app.models import Project, Series
import json

def get_search_values(request):
    #TODO: Keep these values in cache for performance reasons
    search_values = []
    for p in Project.objects.exclude(status="HD"):
        search_values.append({"value": p.name, "url": reverse('project', args=[p.pk])})
    for s in Series.objects.all():
        search_values.append({"value": s.name, "url": reverse('series', args=[s.pk])})
    json_response = json.dumps(sorted(search_values))
    return HttpResponse(json_response, mimetype='application/json')


class TemplateView(generic_views.TemplateView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context

class ListView(generic_views.ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context

class DetailView(generic_views.DetailView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
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
