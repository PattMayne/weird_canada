from django.contrib import admin
from blog.models import Article, Tag, Author, ArticleCategory, ArticleImage
from django_markdown.admin import MarkdownModelAdmin

# Register your models here.

#admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(ArticleCategory)
admin.site.register(ArticleImage)
admin.site.register(Article)
