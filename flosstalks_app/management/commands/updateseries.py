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
import feedparser
import re
from time import strftime
from django.core.management.base import BaseCommand, CommandError
from flosstalks_app.models import Series, Project, Resource, ResourceDownloadURL

class Command(BaseCommand):
    help = 'Updates all series'

    def handle(self, *args, **options):
        if 0 != len(args):
            raise CommandError('This command does not take any argument')
        self.stdout.write("Updating all series:\n")
        for s in Series.objects.all():
            feeds = s.seriesfeedurl_set.all()
            if 0 == len(feeds):
                self.stdout.write("Skipping series that has no feed...")
            else:
                self.stdout.write("\n\n- Updating %d feeds for %s\n" % (len(feeds), s))
#            i = 0
            for f in feeds:
#                if i == 0:
#                    f.url = "file:///home/emilien/devel/flosstalks/data/samples/floss.rss"
#                elif i == 1:
#                    f.url = "file:///home/emilien/devel/flosstalks/data/samples/floss_video_small.rss"
#                elif i == 2:
#                    f.url = "file:///home/emilien/devel/flosstalks/data/samples/floss_video_large.rss"
#                i += 1
                self.stdout.write("%s: %s \n" % (f, f.url))
                d = feedparser.parse(f.url)
                # Check last updated, d["updated"] or d["updated_parsed"]
                for e in d.entries:
                    # Get the project's name
                    rep = re.compile("FLOSS Weekly \d+: (.+)")
                    project_name = rep.match(e.title).groups()[0]
                    self.stdout.write("Project: %s\n" % project_name)
                    # Use the series' url as default base URI for the
                    # resource's ID instead of the feed's base URI
                    e.id = e.id.replace(f.url.rsplit("/", 1)[0], s.url)
                    # Retrieve the project and resource from the database
                    r = None
                    try:
                        p = Project.objects.get(name=project_name)
                        r = Resource.objects.get(external_id=e.id)
                    except Project.DoesNotExist:
                        # Project does not exist, create it
                        p = Project(name=project_name,
                                    description=e.subtitle_detail.value,
                                    status="NW")
                        p.save()
                    except Resource.DoesNotExist:
                        pass
                    if not r:
                        # Resource does not exist, create it
                        r = Resource(name=e.title,
                                     description=e.subtitle_detail.value,
                                     series=s,
                                     status="NW",
                                     external_id=e.id,
                                     length=e.itunes_duration,
                                     pub_date=strftime("%Y-%m-%d %H:%M:%S+00:00", e.updated_parsed),)
                        r.save()
                        # Link the resource to the project
                        r.projects.add(p)
                    # Check if we already know of this download
                    if 0 == len(ResourceDownloadURL.objects.filter(url=e.link)):
                        # Save the download URL
                        u = ResourceDownloadURL(media_type=f.media_type,
                                                format=f.format,
                                                url=e.link,
                                                resource=r,)
                        u.save()
#                    break
#                break
