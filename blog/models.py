from django.db import models
from django.contrib.auth.models import User
#from django_markdown.models import MarkdownField
from indie_db.models import Artist, Work, Track

# Create your models here.


class AudioPlayerLink(models.Model):
    audio_link = models.CharField(max_length=400)
    title = models.CharField(max_length=200)
    artist = models.ManyToManyField(Artist, null=True, blank=True)
    work = models.ForeignKey(Work, null=True, blank=True)
    track = models.ForeignKey(Track, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    main_image = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    caption = models.CharField(max_length=200)
    image_link = models.FileField(upload_to='img/article/%Y/%m/%d', default='img/default.png')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.caption


class ArticleCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.title


class HowCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = "How Category"
        verbose_name_plural = "How Categories"

    def __str__(self):
        return self.title


class RelativeEpoch(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Relative Epoch"

    def __str__(self):
        return self.title


class Author(models.Model):
    authorname = models.CharField(max_length=200, unique=True)
    tagline = models.CharField(max_length=300, default='From the mad mind of ')
    description = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    website = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.authorname


        # The Tag is just a handle to help people search for the right content
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    cover_image = models.FileField(upload_to='img/article/%Y/%m/%d', default='img/default.png')
    author = models.ForeignKey(Author, blank=True, null=True)
    title = models.CharField(max_length=200)
    epoch = models.ForeignKey(RelativeEpoch, null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    article_category = models.ForeignKey(ArticleCategory, blank=True, null=True)
    how_category = models.ManyToManyField(HowCategory, blank=True, null=True)
    body_en = models.TextField(blank=True, null=True)
    body_fr = models.TextField(blank=True, null=True)
    is_review = models.BooleanField(default=False)
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    work_link = models.ForeignKey(Work, null=True, blank=True)
    artist_link = models.ForeignKey(Artist, null=True, blank=True)
    images = models.ManyToManyField(ArticleImage, null=True, blank=True)
    audio_links = models.ManyToManyField(AudioPlayerLink, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_created"]


class Page(models.Model):
    handle = models.CharField(max_length=300, default='Weird Canada')
    title = models.CharField(max_length=300, default='Weird Canada')
    body_en = models.TextField(blank=True, null=True)
    body_fr = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, null=True, blank=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_created"]
