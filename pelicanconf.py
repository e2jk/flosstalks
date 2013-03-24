#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Emilien Klein'
SITENAME = u'FLOSS Talks'
SITEURL = 'http://localhost:8000'
FEED_DOMAIN = 'http://localhost:8000'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = u'en'

# We're not creating a blog, so:
# - Indicate that all pages are static
PAGE_DIR = '.'
# - Point Pelican to a non-existant folder for articles
ARTICLE_DIR = 'dummy'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'
DIRECT_TEMPLATES = ('index', 'about', 'contact',)

FEED_ALL_ATOM = None
THEME = 'themes/flosstalks'

STATIC_URL = '/theme/'

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
