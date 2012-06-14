from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField("Website")
    ohloh_id = models.IntegerField("Ohloh ID")
    STATUSES = (
        ('NW', 'New'),
        ('VF', 'Verified'),
        ('HD', 'Hidden'),
    )
    status = models.CharField(max_length=2, choices=STATUSES)

    def __unicode__(self):
        return self.name

    def number_of_resources(self):
        return self.resource_set.count()

class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField("Website")
    MODES = (
        ('AU', 'Auto-add'),
        ('QU', 'Queue'),
    )
    mode = models.CharField(max_length=2, choices=MODES)

    class Meta:
        verbose_name_plural = "series"

    def __unicode__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project)
    series = models.ForeignKey(Series)
    STATUSES = (
        ('NW', 'New'),
        ('VF', 'Verified'),
        ('PD', 'Pending'),
        ('IG', 'Ignored'),
    )
    status = models.CharField(max_length=2, choices=STATUSES)
    pub_date = models.DateTimeField("Date published")

    def __unicode__(self):
        return self.name

class GenericURL(models.Model):
    MEDIA_TYPES = (
        ('Audio', (
                ('AUS', 'Audio'),
                ('AUL', 'Audio (low quality)'),
                ('AUH', 'Audio (high quality)'),
            )
        ),
        ('Video', (
                ('VIS', 'Video'),
                ('VIL', 'Video (low quality)'),
                ('VIH', 'Video (high quality)'),
            )
        ),
    )
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPES)
    url = models.URLField()

class SeriesFeedURL(GenericURL):
    series = models.ForeignKey(Series)

    class Meta:
        verbose_name = "series' feed URL"
        verbose_name_plural = "series' feed URLs"

    def __unicode__(self):
        return "%s's %s feed" % (self.series.name, self.get_media_type_display())

class ResourceDownloadURL(GenericURL):
    resource = models.ForeignKey(Resource)
    length = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "resource download URL"
        verbose_name_plural = "resource download URLs"

    def __unicode__(self):
        return "%s for %s" % (self.get_media_type_display(), self.resource.name)

