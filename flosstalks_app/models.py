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
import datetime
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField("Website", null=True, blank=True)
    ohloh_id = models.IntegerField("Ohloh ID", null=True, blank=True)
    STATUSES = (
        ('NW', 'New'),
        ('VF', 'Verified'),
        ('HD', 'Hidden'),
    )
    status = models.CharField(max_length=2, choices=STATUSES, default="VF")

    def __unicode__(self):
        return self.name

    def number_of_resources(self):
        return self.resource_set.count()

class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField("Website", null=True, blank=True)
    MODES = (
        ('AU', 'Auto-add'),
        ('QU', 'Queue'),
    )
    mode = models.CharField(max_length=2, choices=MODES, default="QU")

    class Meta:
        verbose_name_plural = "series"

    def __unicode__(self):
        return self.name

    def number_of_resources(self):
        return self.resource_set.count()

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    projects = models.ManyToManyField(Project)
    series = models.ForeignKey(Series)
    STATUSES = (
        ('NW', 'New'),
        ('VF', 'Verified'),
        ('PD', 'Pending'),
        ('IG', 'Ignored'),
    )
    status = models.CharField(max_length=2, choices=STATUSES, default="VF")
    external_id = models.CharField(max_length=200)
    length = models.CharField(max_length=10, null=True, blank=True)
    pub_date = models.DateTimeField("Date published"
                                    , default=datetime.datetime.now())

    def __unicode__(self):
        return self.name

    def list_of_projects(self):
        projects = []
        for p in self.projects.get_query_set():
            projects.append(p.name)
        return ", ".join(projects)

class GenericURL(models.Model):
    MEDIA_TYPES = (
        ('Audio', (
                ('AUS', 'Audio'),
                ('AUL', 'Audio (low quality)'),
                ('AUH', 'Audio (high quality)'),
            )
        ),
        ('Video', (
                ('VIS', 'Video'),
                ('VIL', 'Video (low quality)'),
                ('VIH', 'Video (high quality)'),
            )
        ),
    )
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPES)
    url = models.URLField()

class SeriesFeedURL(GenericURL):
    series = models.ForeignKey(Series)

    class Meta:
        verbose_name = "series' feed URL"
        verbose_name_plural = "series' feed URLs"

    def __unicode__(self):
        return "%s's %s feed" % (self.series.name, self.get_media_type_display())

class ResourceDownloadURL(GenericURL):
    resource = models.ForeignKey(Resource)

    class Meta:
        verbose_name = "resource download URL"
        verbose_name_plural = "resource download URLs"

    def __unicode__(self):
        return "%s for %s" % (self.get_media_type_display(), self.resource.name)

