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

# Inspired by http://djangosnippets.org/snippets/234/
from django.core.management.base import BaseCommand
from flosstalks import settings
from django.db import transaction, connection
import os

class Command(BaseCommand):
    help = 'Vacuums the database, i.e. rebuilds the entire database'

    def vacuum_db(self):
        cursor = connection.cursor()
        cursor.execute("VACUUM")
        connection.close()

    def handle(self, *args, **options):
        self.stdout.write("Vacuuming database...\n")
        before = os.stat(settings.DATABASES["default"]["NAME"]).st_size
        self.stdout.write("Size before: %s bytes\n" % before)
        self.vacuum_db()
        after = os.stat(settings.DATABASES["default"]["NAME"]).st_size
        self.stdout.write("Size after: %s bytes\n" % after)
        self.stdout.write("Reclaimed: %s bytes\n" % (before - after))
