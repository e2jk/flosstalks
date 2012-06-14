from flossprojects_app.models import Series, SeriesFeedURL, Project, Resource
from django.contrib import admin

class SeriesFeedURLInline(admin.TabularInline):
    model = SeriesFeedURL
    extra = 2

class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesFeedURLInline]

admin.site.register(Series, SeriesAdmin)
admin.site.register(Project)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "series")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]
    date_hierarchy = "pub_date"

admin.site.register(Resource, ResourceAdmin)
