from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
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
    description = models.CharField(max_length=2000)
    url = models.URLField()
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
    description = models.CharField(max_length=2000)
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
    url = models.URLField()
    MEDIA_TYPES = (
        ('AU', 'Audio'),
        ('VI', 'Video'),
    )
    media_type = models.CharField(max_length=2, choices=MEDIA_TYPES)

class SeriesFeedURL(GenericURL):
    series = models.ForeignKey(Series)

class ResourceDownloadURL(GenericURL):
    resource = models.ForeignKey(Resource)
    length = models.CharField(max_length=10)

