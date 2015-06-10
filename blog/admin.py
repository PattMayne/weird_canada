from django.contrib import admin
from blog.models import Entry, Tag, Author

# Register your models here.
admin.site.register(Entry)
admin.site.register(Author)
admin.site.register(Tag)
