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
from operator import neg
from django.core.management.base import BaseCommand, CommandError
from django.utils.http import urlquote
from flosstalks_app.models import Series, Project, Resource, ResourceDownloadURL

class GenericSeries(object):
    def __init__(self, feeds):
        self.feeds = feeds

    def testmode(self):
        i = 0
        for f in self.feeds:
            f.url = self.sample_feeds[i]
            i += 1

    def get_entry_link(self, entry):
        print "NOT IMPLEMENTED: get_entry_link"
        return None

    def get_project_name_and_entry_id(self, series, feed, entry):
        print "NOT IMPLEMENTED: get_project_name_and_entry_id"
        return None

    def get_resource_link(self, entry):
        print "NOT IMPLEMENTED: get_resource_link"
        return None

    def get_nice_url(self, value):
        # Returns a string that is safe to use as a nice url
        return urlquote(value[:99] # nice_url fields have max_length=100
                        .lower()
                        .replace(" ", "-")
                        .replace("/", "-")
                        .replace("---", "-")
                        .replace("--", "-"))


class FLOSSWeekly(GenericSeries):
    sample_feeds = [
        "file:///home/emilien/devel/flosstalks/data/samples/floss.rss",
        "file:///home/emilien/devel/flosstalks/data/samples/floss_video_small.rss",
        "file:///home/emilien/devel/flosstalks/data/samples/floss_video_large.rss",
    ]
    def __init__(self, feeds):
        super(FLOSSWeekly, self).__init__(feeds)

    def get_entry_link(self, entry):
        return entry.link

    def get_project_name_and_entry_id(self, series, feed, entry):
        rep = re.compile("FLOSS Weekly \d+: (.+)")
        return (rep.match(entry.title).groups()[0],
                # Use the series' url as default base URI for the
                # resource's ID instead of the feed's base URI
                entry.id.replace(feed.url.rsplit("/", 1)[0], series.url))

    def get_resource_link(self, entry):
        return entry.comments


class Sourcetrunk(GenericSeries):
    sample_feeds = [
        "file:///home/emilien/devel/flosstalks/data/samples/sourcetrunk_ogg.rss",
        "file:///home/emilien/devel/flosstalks/data/samples/sourcetrunk.rss",
    ]
    def __init__(self, feeds):
        super(Sourcetrunk, self).__init__(feeds)

    def get_entry_link(self, entry):
        return entry.links[1].href

    def get_project_name_and_entry_id(self, series, feed, entry):
        rep = re.compile("(\d+) Sourcetrunk : (.+)")
        return (rep.match(entry.title).groups()[1],
                # Create a unique resource ID, since there's none
                # specified in Sourcetrunk's feed
                "%s%s" % (series.url, rep.match(entry.title).groups()[0]))

    def get_resource_link(self, entry):
        return entry.feedburner_origlink


class TheChangelog(GenericSeries):
    sample_feeds = [
        "file:///home/emilien/devel/flosstalks/data/samples/thechangelog.rss",
    ]
    def __init__(self, feeds):
        super(TheChangelog, self).__init__(feeds)

    def get_entry_link(self, entry):
        return entry.link

    def get_project_name_and_entry_id(self, series, feed, entry):
        base_regex = "Episode [\d\.]+ - (.+)"
        rep = re.compile("%s with .+" % base_regex)
        if rep.match(entry.title):
            title = rep.match(entry.title).groups()[0]
        else:
            # The episode title does not contain " with YYY"
            rep = re.compile(base_regex)
            if rep.match(entry.title):
                title = rep.match(entry.title).groups()[0]
            else:
                # No episode number (probably not a project's resource...)
                title = entry.title
        # Strip the following bits if the name ends in it
        for s in (", and more", " and more", ","):
            if title.endswith(s):
                title = title[:neg(len(s))]
        title = title.strip()
        return (title, entry.id)

    def get_resource_link(self, entry):
        return entry.link


class Command(BaseCommand):
    help = 'Updates all series'

    def handle(self, *args, **options):
        testmode = False
        if 1 == len(args) and "testmode" == args[0]:
            testmode = True
            self.stdout.write("TEST MODE ON\n\n")
        elif 0 != len(args):
            raise CommandError('Invalid argument')
        self.stdout.write("Updating all series:\n")
        for s in Series.objects.all():
            feeds = s.seriesfeedurl_set.all()
            ss = None
            if "FLOSS Weekly" == s.name:
                ss = FLOSSWeekly(feeds)
            elif "Sourcetrunk" == s.name:
                ss = Sourcetrunk(feeds)
            elif "The Changelog" == s.name:
                ss = TheChangelog(feeds)
            else:
                self.stdout.write("\n\nWarning: Series %s not supported yet!\n" % s.name)
                continue
            if testmode:
                # In test mode, use the sample RSS feeds instead of the real ones
                ss.testmode()
            if 0 == len(feeds):
                self.stdout.write("Skipping series that has no feed...\n")
            else:
                self.stdout.write("\n\n- Updating %d feeds for %s" % (len(feeds), s))
            for f in ss.feeds:
                self.stdout.write("\n\n%s (%s): %s" % (f, f.format, f.url))
                d = feedparser.parse(f.url)
                # Check last updated, d["updated"] or d["updated_parsed"]
                for e in d.entries:
                    self.stdout.write("\n%s:\t" % e.title)
                    # Check if this download is already known
                    entry_link = ss.get_entry_link(e)
                    if 0 != len(ResourceDownloadURL.objects.filter(url=entry_link)):
                        self.stdout.write(u"\u2714")
                        continue
                    self.stdout.write("U")
                    u = ResourceDownloadURL(media_type=f.media_type,
                                            format=f.format,
                                            url=entry_link,)
                    # Get the project's name and the entry's id
                    (project_name, entry_id) = ss.get_project_name_and_entry_id(s, f, e)
                    # Check if this resource is already known
                    try:
                        r = Resource.objects.get(external_id=entry_id)
                        u.resource = r
                        u.save()
                        # The new download url is linked to the
                        # already-existing resource, nothing left to do
                        continue
                    except Resource.DoesNotExist:
                        self.stdout.write(" R")
                    r = Resource(name=e.title,
                                 description=e.subtitle_detail.value,
                                 url=ss.get_resource_link(e),
                                 series=s,
                                 status="NW",
                                 external_id=entry_id,
                                 pub_date=strftime("%Y-%m-%d %H:%M:%S+00:00", e.updated_parsed),)
                    if e.has_key("itunes_duration"):
                        r.length = e.itunes_duration
                    r.save()
                    # Link the download URL to the resource
                    u.resource = r
                    u.save()
                    # Check if this project is already known
                    try:
                        p = Project.objects.get(name=project_name)
                        # Link the resource to the project
                        r.projects.add(p)
                        continue
                    except Project.DoesNotExist:
                        self.stdout.write(" P")
                        # Project does not exist, create it
                        p = Project(name=project_name,
                                    description=e.subtitle_detail.value,
                                    status="NW")
                        # Give this project a nice URL only if not yet used
                        # for either a project or a series
                        nu = ss.get_nice_url(project_name)
                        if 0 == Project.objects.filter(nice_url=nu).count() and \
                           0 == Series.objects.filter(nice_url=nu).count():
                            p.nice_url = nu
                        else:
                            self.stdout.write("\nWarning: nice url '/%s' already in use!\n" % nu)
                        p.save()
                        # Link the resource to the project
                        r.projects.add(p)
            self.stdout.write("\n")
