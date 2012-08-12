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

# Series-related admin
class SeriesFeedURLInline(admin.TabularInline):
    model = SeriesFeedURL
    extra = 2

class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesFeedURLInline]
    list_display = ("name", "number_of_resources")

admin.site.register(Series, SeriesAdmin)


# Project-related admin
class ProjectAdmin(admin.ModelAdmin):
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
