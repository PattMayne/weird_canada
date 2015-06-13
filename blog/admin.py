from django.contrib import admin
from blog.models import Article, Tag, Author

# Register your models here.
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Tag)
