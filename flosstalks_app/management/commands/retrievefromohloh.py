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
import urllib2
from xml.dom import minidom
from django.core.management.base import BaseCommand, CommandError
from flosstalks_app.models import Project
from flosstalks.DO_NOT_SHARE import OHLOH_API_KEY

class Command(BaseCommand):
    help = 'Retrieves information about new projects from ohloh.net'

    def handle(self, *args, **options):
        if 0 != len(args):
            raise CommandError('Invalid argument')
        self.stdout.write("Retrieving project information from Ohloh for new projects:\n\n")

        # Query for new projects for which the Ohloh ID is known (set manually)
        projects = Project.objects.filter(status="NW") \
                                  .exclude(skip_ohloh=True) \
                                  .exclude(ohloh_id=None)
        self.stdout.write("Querying %d projects by Ohloh ID\n\n" % len(projects))
        for p in projects:
            self.stdout.write("Project %d: %s (Ohloh ID %d)\n" % (p.id, p.name, p.ohloh_id))
            url = "https://www.ohloh.net/p/%(ohloh_id)d.xml?api_key=%(api_key)s" % {
                    "ohloh_id": p.ohloh_id,
                    "api_key": OHLOH_API_KEY,
            }
            data = self.get_result(url)
            if data:
                self.process_result(data, p, skip_name_check=True)

        # Search all new projects on name
        projects = Project.objects.filter(status="NW") \
                                  .exclude(skip_ohloh=True)
        self.stdout.write("\n\nSearching for %d projects by name\n\n" % len(projects))
        for p in projects:
            self.stdout.write("Project %d: %s\n" % (p.id, p.name))
            url = "http://www.ohloh.net/projects.xml?query=%(name)s&api_key=%(api_key)s" % {
                    "name": p.name,
                    "api_key": OHLOH_API_KEY,
            }
            data = self.get_result(url)
            if data:
                self.process_result(data, p)

    def get_result(self, url):
            try:
                data = urllib2.urlopen(url).read()
            except urllib2.HTTPError, e:
                self.stdout.write("\nHTTP error: %d\n\n" % e.code)
                return None
            except urllib2.URLError, e:
                self.stdout.write("\nNetwork error: %s\n\n" % e.reason.args[1])
                return None
            return data

    def process_result(self, data, p, skip_name_check=False):
        doc = minidom.parseString(data)
        if "success" == self.get_info_from_XML("status", doc):
            if len(doc.getElementsByTagName("project")) > 0:
                # Only consider the first project
                self.item = doc.getElementsByTagName("project")[0]
                name = self.get_info_from_XML("name")
                if skip_name_check or name.lower() == p.name.lower():
                    # Only consider a match if the project names are identical
                    # or if we were doing a direct query on Ohloh ID
                    self.stdout.write("    Found on Ohloh!\n\n")
                    # Update the project with the information from Ohloh!
                    p.ohloh_id = self.get_info_from_XML("id")
                    p.description = self.get_info_from_XML("description")
                    p.description_source = self.get_info_from_XML("html_url")
                    p.url = self.get_info_from_XML("homepage_url")
                    if "no_logo.png" != self.get_info_from_XML("medium_logo_url"):
                        # Only save the logo if there is a valid logo 
                        p.logo_url = self.get_info_from_XML("medium_logo_url")
                    # Mark the project as Pending. This allows the project to directly
                    # be visible, but we can easily check if all seems fine.
                    p.status = "PD"
                    # Save the project
                    p.save()
                    return True
            # If we get here, it means we couldn't fine a proper project on Ohloh
            # This project must not be searched again on Ohloh, it will have to be done manually
            self.stdout.write("    Not found on Ohloh, skipping...\n")
            p.skip_ohloh = True
            p.save()
            return False

    def get_info_from_XML(self, node, item=None):
        if not item:
            item = self.item
        info = None
        node = item.getElementsByTagName(node)
        if len(node) > 0 and len(node[0].childNodes) > 0:
            return node[0].childNodes[0].data
        return info
