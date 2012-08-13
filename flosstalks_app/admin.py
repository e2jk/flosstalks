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
from flosstalks_app.models import Series, SeriesFeedURL, Project, \
        Resource, ResourceDownloadURL
from django.contrib import admin
from django.conf.urls import patterns
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django import forms
from django.forms.formsets import formset_factory

# Series-related admin
class SeriesFeedURLInline(admin.TabularInline):
    model = SeriesFeedURL
    extra = 2

class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesFeedURLInline]
    list_display = ("name", "number_of_resources")

admin.site.register(Series, SeriesAdmin)


# Project-related admin
class DeduplicateProjectForm(forms.Form):
    name = forms.CharField(max_length=100)
    nice_url = forms.SlugField(max_length=100)

class ProjectModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ProjectModelAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^deduplicate/(?P<project_id>\d+)/$', self.admin_site.admin_view(self.deduplicate_project))
        )
        return my_urls + urls

    def slugify(self, value):
        #TODO: copied from updateseries. This should be in a unique place
        # Returns a string that is safe to use as a nice url
        return urlquote(value[:99] # nice_url fields have max_length=100
                        .lower()
                        .replace(" ", "-")
                        .replace("/", "-")
                        .replace("---", "-")
                        .replace("--", "-"))

    def deduplicate_project(self, request, project_id):
        # Allows to split a project into multiple that are linked to the
        # same resources
        original_project = get_object_or_404(Project, pk=project_id)

        if request.method == 'POST': # If the form has been submitted...
            # Get a formset bound to the POST data
            ProjectFormSet = formset_factory(DeduplicateProjectForm)
            formset = ProjectFormSet(request.POST)
            if formset.is_valid():
                # All validation rules pass, retrieve the list of resources
                # that were linked to the original project
                resources = original_project.resource_set.all()
                success = False
                # Process the data in formset.cleaned_data
                for cleaned_data in formset.cleaned_data:
                    if cleaned_data:
                        project_name = cleaned_data["name"].strip()
                        try:
                            # Check if it's an already-known project
                            p = Project.objects.get(name=project_name)
                            if "VF" == p.status:
                                 # If the project was already verified,
                                 # bump it back to Pending
                                 p.status = "PD"
                                 p.save()
                        except Project.DoesNotExist:
                            # Create a new project
                            p = Project(name=project_name,
                                        description=u"Empty description",
                                        status="NW")
                            # Check if the nice url is not already in use
                            nu = cleaned_data["nice_url"].strip()
                            if 0 == Project.objects.filter(nice_url=nu).count() and \
                               0 == Series.objects.filter(nice_url=nu).count():
                                p.nice_url = nu
                            # Save the newly created project
                            p.save()
                        # Link the [new] project to all the resources of
                        # the original project
                        for r in resources:
                            r.projects.add(p)
                        success = True
                    else:
                        # An empty string, nothing to do
                        pass

                if success:
                    # Delete the original project if at least one new
                    # project got created
                    original_project.delete()
                # Redirect after POST
                return HttpResponseRedirect("/admin/flosstalks_app/project/deduplicate/%d/" % (int(project_id) + 1))
        else:
            # This is a GET
            # Try to split the names of the projects
            new_projects_names = [original_project.name]
            if ", " in original_project.name:
                # Split the project names on ", "
                new_projects_names = original_project.name.split(", ")
            if " and " in new_projects_names[-1]:
                # Split the last 2 project names on " and "
                new_projects_names.extend(new_projects_names[-1].split(" and "))
                # Remove the one containing " and " since it's now split
                new_projects_names.pop(-3)

            new_projects = []
            for p in new_projects_names:
                new_projects.append({"name": p.strip(),
                                     "nice_url": self.slugify(p.strip())})

            ProjectFormSet = formset_factory(DeduplicateProjectForm, extra=3)
            formset = ProjectFormSet(initial=new_projects)

        return render_to_response(
            "admin/projects/deduplicate.html",
            {
             "original_project" : original_project,
             "formset": formset,
            },
            RequestContext(request, {}),
        )

class ProjectAdmin(ProjectModelAdmin):
    list_display = ("name", "status", "number_of_resources")
    list_filter = ["status", "skip_ohloh"]
    search_fields = ["name", "description"]

admin.site.register(Project, ProjectAdmin)


# Resource-related admin
class ResourceDownloadURLInline(admin.TabularInline):
    model = ResourceDownloadURL
    extra = 1

class ResourceAdmin(admin.ModelAdmin):
    inlines = [ResourceDownloadURLInline]
    list_display = ("name", "list_of_projects", "series")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]
    date_hierarchy = "pub_date"

admin.site.register(Resource, ResourceAdmin)
