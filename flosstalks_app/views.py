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
import django.views.generic as generic_views

class TemplateView(generic_views.TemplateView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context

class ListView(generic_views.ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context

class DetailView(generic_views.DetailView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context
