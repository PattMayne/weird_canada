from django.contrib import admin
from blog.models import Article, Tag, Author, ArticleCategory, RelativeEpoch

# Register your models here.
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(RelativeEpoch)
admin.site.register(ArticleCategory)
#admin.site.register(ArticleImage)
