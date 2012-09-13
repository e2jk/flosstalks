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
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.forms import ModelForm
from flosstalks_app.models import Project, Series, Resource, ResourceDownloadURL
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

        if self.template_name in ("projects_list.html", "series_list.html"):
            # Calculate when to start the new column
            context['new_column_index'] = ((len(context[self.template_name[:-5]]) + 1) / 2)

        if "projects_list.html" == self.template_name:
            pages = []
            num_pages = context['paginator'].num_pages
            current_page = context['page_obj'].number
            if current_page > 1:
                pages.append(1)
            if current_page > 4:
                pages.append("...")
            if current_page > 3:
                pages.append(current_page - 2)
            if current_page > 2:
                pages.append(current_page - 1)
            pages.append(current_page)
            if current_page + 1 < num_pages:
                pages.append(current_page + 1)
            if current_page + 2 < num_pages:
                pages.append(current_page + 2)
            if current_page + 3 < num_pages:
                pages.append("...")
            if current_page < num_pages:
                pages.append(num_pages)
            context['pages_list'] = pages

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

        if "series_detail.html" == self.template_name:
            series_list = context['series'].resource_set \
                                           .exclude(status="IG") \
                                           .order_by("-name")
            context['series_list'] = series_list
            context['new_column_index'] = (len(series_list) + 1) / 2

        return context

class NewResourceForm(ModelForm):
    class Meta:
        model = Resource
        exclude = ('projects', 'series', 'status', 'external_id', 'length', 'pub_date')

class ResourceDownloadURLForm(ModelForm):
    class Meta:
        model = ResourceDownloadURL
        exclude = ('resource')

def project_add_resource(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST': # If the form has been submitted...
        resource_form = NewResourceForm(request.POST, prefix="resource")
        resource_download_url_form = ResourceDownloadURLForm(request.POST, prefix="download")
        if resource_form.is_valid():
            # All NewResourceForm validation rules pass
            success = True
            # Process the data in resource_form.cleaned_data
            new_resource = Resource(name=resource_form.cleaned_data["name"],
                                    description=resource_form.cleaned_data["description"],
                                    url=resource_form.cleaned_data["url"],
                                    status="SG"
            )
            # We've got our new resource, now let's check if the download
            # information provided is valid. If the download URL is filled
            # and there is an error, show the error messages.
            # If the download URL is empty, just ignore it.
            u = None
            if resource_download_url_form.is_valid():
                # All ResourceDownloadURLForm validation rules pass
                u = ResourceDownloadURL(media_type=resource_download_url_form.cleaned_data["media_type"],
                                        format=resource_download_url_form.cleaned_data["format"],
                                        url=resource_download_url_form.cleaned_data["url"])
            elif resource_download_url_form.data["download-url"]:
                # The download URL is populated, yet some of the info related
                # to the download URL is not valid, so show the error message
                success = False
            if success:
                # Create the new resource
                new_resource.save()
                new_resource.projects.add(project)
                if u:
                    # Create the new download URL
                    u.resource = new_resource
                    u.save()
                # Redirect after POST to show success message
                return HttpResponseRedirect('/p/%d/resource-added' % project.pk)
    else:
        # Unbound forms
        resource_form = NewResourceForm(prefix="resource")
        resource_download_url_form = ResourceDownloadURLForm(prefix="download")

    c = RequestContext(request, {
        'resource_form': resource_form,
        "resource_download_url_form": resource_download_url_form,
        'project': project,
    })
    return render_to_response('project_add_resource.html', c)

def search(request):
    search_term = request.GET.get("q")
    projects = Project.objects.filter(name__icontains=search_term) \
                              .exclude(status="HD") \
                              if search_term else None
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

            series_list = series.resource_set.exclude(status="IG") \
                                             .order_by("-name")
            c = RequestContext(request, {
                'series': series,
                "series_list": series_list,
                "new_column_index": (len(series_list) + 1) / 2,
            })
            return render_to_response('series_detail.html', c)
        except Series.DoesNotExist:
            # Not a valid nice url
            #TODO: This breaks Django's automatic redirect from /r/22 to /r/22/
            raise Http404
