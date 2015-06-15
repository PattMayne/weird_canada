from django.db import models

from blog.models import Author

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


class Style(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class URL(models.Model):
    link = models.CharField(max_length=400)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    deathdate = models.DateField(null=True, blank=True)
    group = models.BooleanField(default=False)
    members = models.ManyToManyField('self')
    author = models.ForeignKey(Author, null=True, blank=True)
    website = models.ForeignKey(URL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Contributor(models.Model):
    contributing_artist = models.ForeignKey(Artist, null=True, blank=True)
    alternate_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)


class ProductionCompany(models.Model):
    name = models.CharField(max_length=200)
    website = models.ForeignKey(URL)
    location = models.CharField(max_length=200)
    author = models.ForeignKey(Author, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Production Companies"
        ordering = ["name"]


class Work(models.Model):
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    created = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=200)
    production_company = models.ForeignKey(ProductionCompany, blank=True, null=True)
    self_published = models.BooleanField(default=False)
    creator = models.ForeignKey(Artist, null=True, blank=True)
    website = models.ForeignKey(URL, null=True, blank=True)
    styles = models.ManyToManyField(Style, null=True, blank=True)
    contributors = models.ManyToManyField(Contributor, null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Work of Art"
        verbose_name_plural = "Works of Art"

    def __str__(self):
        return self.title
