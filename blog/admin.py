from django.contrib import admin
from blog.models import Article, Tag, Author, ArticleCategory, ArticleImage
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

# Register your models here.


class EntryAdmin(MarkdownModelAdmin):
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}


#admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(ArticleCategory)
admin.site.register(ArticleImage)
admin.site.register(Article, EntryAdmin)
