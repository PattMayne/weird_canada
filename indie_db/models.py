from django.db import models

from django.contrib.auth.models import User

# Create your models here.

'''
    CLASSES:
        -Work
        -MusicAlbum
        -WrittenWork
        -VideoFilm
        -Performance

        -Artist
        -ArtistSingle
        -ArtistGroup
        -Contributor
        -Role
        -ProductionCompany
'''


class Track(models.Model):
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=12)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']


class Format(models.Model):
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.label


class WorkCategory(models.Model):
    title = models.CharField(max_length=200)
    description_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Work of Art Category"
        verbose_name_plural = "Work of Art Categories"

    def __str__(self):
        return self.title


class Style(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class URL(models.Model):
    link = models.CharField(max_length=400)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.link


class Artist(models.Model):
    prof_image = models.FileField(upload_to='img/artist/%Y/%m/%d', default='img/default.png')
    name = models.CharField(max_length=200)
    description_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    deathdate = models.DateField(null=True, blank=True)
    group = models.BooleanField(default=False)
    worked_with = models.ManyToManyField('self', null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    website = models.ForeignKey(URL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Contributor(models.Model):
    contributing_artist = models.ForeignKey(Artist, null=True, blank=True)
    alternate_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.contributing_artist.name


class ProductionCompany(models.Model):
    name = models.CharField(max_length=200)
    website = models.ForeignKey(URL, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    styles = models.ManyToManyField(Style, null=True, blank=True)
    formats = models.ManyToManyField(Format, null=True, blank=True)
    description_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Production Companies"
        ordering = ["name"]


class Work(models.Model):
    cover_image = models.FileField(upload_to='img/work/%Y/%m/%d', default='img/default.png')
    work_category = models.ForeignKey(WorkCategory, null=True, blank=True)
    title = models.CharField(max_length=200)
    description_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    extra_data = models.TextField(null=True, blank=True)
    created = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=200)
    production_company = models.ForeignKey(ProductionCompany, blank=True, null=True)
    self_published = models.BooleanField(default=False)
    creator = models.ForeignKey(Artist, null=True, blank=True)
    website = models.ForeignKey(URL, null=True, blank=True)
    styles = models.ManyToManyField(Style, null=True, blank=True)
    formats = models.ManyToManyField(Format, null=True, blank=True)
    contributors = models.ManyToManyField(Contributor, null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    tracklist = models.ManyToManyField(Track, null=True, blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Work of Art"
        verbose_name_plural = "Works of Art"

    def __str__(self):
        return self.title
