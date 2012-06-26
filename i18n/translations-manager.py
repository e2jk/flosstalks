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
import os, shutil, sys

################################
# Launchpad needs all the .po files to be in the same folder as the .pot
# template file, and each po file to be named "XX.po" (where XX is the ISO 639
# code of the language). For FLOSS Talks, those files are located in the
# "./i18n" folder. But Django needs them to be in "./locale/XX/LC_MESSAGES"
# in order to be used, so this script will place the translations in the
# right place and update the .pot template that will in turn be fed back to
# Launchpad to allow the new strings to be translated. Note that the .pot
# file is actually just the English .po file renamed as .pot, and is
# generated each time this script is run.
#
# Based on an original script from the Issue Tracker Tracker project:
# https://launchpad.net/issuetrackertracker
################################
def main():
    poFolder = "./i18n"
    # Check if the folder exists, i.e. dotLangFolder is a valid folder
    if not os.path.isdir(poFolder):
        # The folder does not exist, we are probably not running the script from the root of the repository
        # Exit with an error message
        print "ERROR: Please run this script from the root of the repository."
        exit(-1)

    sys.path.append("./flosstalks")
    import settings

    allFiles = os.listdir(poFolder)
    languages = []
    for f in allFiles:
        if f[-3:] == ".po":
            languages.append(f.replace(".po", ""))

    # Get the list of languages in the conf/settings.py file
    confLangs = []
    for ll in settings.LANGUAGES:
        confLangs.append(ll[0])

    localeFolder = "./locale/"
    langFolder = localeFolder + "%s/LC_MESSAGES"
    for l in languages:
        # Try to create the tree structure, in case it is a new language
        try: os.makedirs(langFolder % l)
        except: pass
        # Check if the language is enabled in './flosstalks/settings.py'
        if l not in confLangs:
            print "NOTE: '%s' is a new language, it should be added to './flosstalks/settings.py'" % l
        # Copy the XX.po file to the django.po, where Django can access it
        src = "%s/%s.po" % (poFolder, l)
        dst = "%s/django.po" % (langFolder % l)
        shutil.copy(src, dst)

    # Create the "en" folder (will be used to create the .pot template)
    try: os.makedirs("./locale/en")
    except: pass
    # Update the translations
    os.system("python manage.py makemessages -a")

    # Update the .pot template (i.e. move the "en" .po file to flosstalks.pot)
    # Only do that if real changes have been made to the translations
    # Make sure we start with a clean .pot file
    os.system("git checkout -- i18n/flosstalks.pot")
    src = "%s/django.po" % (langFolder % "en")
    dst = "%s/flosstalks.pot" % poFolder

    cmd = "diff --ignore-matching-lines='POT-Creation-Date' %s %s > /dev/null" % (src, dst)
    if os.system(cmd):
        # The diff returns a non-null value, so there is at least one
        # meaningful difference between the .pot and the English .po file
        print "Changes have been made to the translation template"
        shutil.copy(src, dst)

    #TODO: Check if the charset in the .pot file should be set to "utf-8"

    # Remove the "en" folder
    shutil.rmtree(localeFolder + "en")

    # Compile all the .mo files
    os.system("python manage.py compilemessages")

    # DONE!

if __name__ == '__main__':
    main()
