from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    ohloh_name = models.CharField(max_length=100)
    STATUSES = (
        ('NW', 'New'),
        ('VF', 'Verified'),
        ('HD', 'Hidden'),
    )
    status = models.CharField(max_length=2, choices=STATUSES)
    def __unicode__(self):
        return self.name

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
    def __unicode__(self):
        return "%s's %s feed" % (self.series.name, self.get_media_type_display())

class ResourceDownloadURL(GenericURL):
    resource = models.ForeignKey(Resource)
    length = models.CharField(max_length=10)

