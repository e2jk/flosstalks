import django.views.generic as generic_views

class TemplateView(generic_views.TemplateView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['this_page'] = self.template_name.split(".html")[0]
        return context
