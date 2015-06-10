from django.db import models
from django.contrib.auth.models import User
#from django_markdown.models import MarkdownField
from indie_db.models import Artist, Work

# Create your models here.


class Author(models.Model):
    authorname = models.CharField(max_length=200, unique=True)
    tagline = models.CharField(max_length=300)
    description = models.TextField()
    #profile_image = models.FileField(upload_to='prof_img/user/%Y/%m/%d', default='prof_img/user/default.jpg')
    user = models.OneToOneField(User, blank=True, null=True)
    website = models.CharField(max_length=400)

    def __str__(self):
        return self.authorname


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class Entry(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.CharField(max_length=200)
    body_en = models.TextField()
    body_fr = models.TextField()
    #body_en = MarkdownField()
    #body_fr = MarkdownField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    work_link = models.ForeignKey(Work, null=True, blank=True)
    artist_link = models.ForeignKey(Artist, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-created"]
