#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Emilien Klein'
SITENAME = u'FLOSS Talks'
SITEURL = ''

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = u'en'

PAGE_DIR = '.'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'
DIRECT_TEMPLATES = ('index',)

FEED_ALL_ATOM = None
THEME = 'simple'

DISPLAY_PAGES_ON_MENU = False

# Blogroll
LINKS = (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False
