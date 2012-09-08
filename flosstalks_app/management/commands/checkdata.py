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
from django.core.management.base import BaseCommand, CommandError
from flosstalks_app.models import Project, Series

class Command(BaseCommand):
    help = 'Checks that the database contains valid information'

    def handle(self, *args, **options):
        if 0 != len(args):
            raise CommandError('Invalid argument')
        self.stdout.write("Checking that the database contains valid information\n\n")

        # Check that there are no duplicate nice url
        # Add the static urls (see ../../urls.py for the values)
        static_urls = ["about", "contact", "projects", "series", "search",
                       "search-values.json"]
        nu = list(static_urls)
        # Nice urls from projects
        for p in Project.objects.all():
            if p.nice_url:
                nu.append(p.nice_url)
        # Nice urls from series
        for s in Series.objects.all():
            if s.nice_url:
                nu.append(s.nice_url)
        # Determine which values are duplicates
        # Found on http://stackoverflow.com/questions/685671
        duplicates = set()
        found = set()
        for item in nu:
            if item in found:
                duplicates.add(item)
            else:
                found.add(item)
        # Display the result
        if len(duplicates) == 0:
            self.stdout.write("There are no duplicate nice urls\n")
        else:
            self.stdout.write("There are %d duplicate nice urls:\n" % len(duplicates))
            for d in duplicates:
                self.stdout.write("%s\n" % d)
                if d in static_urls:
                    self.stdout.write("\t- Static page\n")
                for p in Project.objects.filter(nice_url=d):
                    self.stdout.write("\t- Project %d: %s\n" % (p.id, p.name))
                for s in Series.objects.filter(nice_url=d):
                    self.stdout.write("\t- Series %d: %s\n" % (s.id, s.name))
