from flossprojects_app.models import Series, SeriesFeedURL
from django.contrib import admin

class SeriesFeedURLInline(admin.TabularInline):
    model = SeriesFeedURL
    extra = 2

class SeriesAdmin(admin.ModelAdmin):
    inlines = [SeriesFeedURLInline]

admin.site.register(Series, SeriesAdmin)

