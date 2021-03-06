from django.contrib import admin
from blog.models import Article, Tag, Author, ArticleCategory, RelativeEpoch, HowCategory, Page, AudioPlayerLink

# Register your models here.
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(RelativeEpoch)
admin.site.register(ArticleCategory)
admin.site.register(HowCategory)
admin.site.register(Page)
admin.site.register(AudioPlayerLink)
