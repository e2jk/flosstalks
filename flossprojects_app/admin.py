from flossprojects_app.models import Series, SeriesFeedURL, Project, \
        Resource, ResourceDownloadURL
from django.contrib import admin

class SeriesFeedURLInline(admin.TabularInline):
    model = SeriesFeedURL
    extra = 2

class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesFeedURLInline]

admin.site.register(Series, SeriesAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_resources")

admin.site.register(Project, ProjectAdmin)

class ResourceDownloadURLInline(admin.TabularInline):
    model = ResourceDownloadURL
    extra = 1

class ResourceAdmin(admin.ModelAdmin):
    inlines = [ResourceDownloadURLInline]
    list_display = ("name", "project", "series")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]
    date_hierarchy = "pub_date"

admin.site.register(Resource, ResourceAdmin)
