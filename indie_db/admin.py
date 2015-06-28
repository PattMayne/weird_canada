from django.contrib import admin
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany, WorkCategory, Style

# Register your models here.
admin.site.register(Artist)
admin.site.register(Work)
admin.site.register(Style)
admin.site.register(WorkCategory)
admin.site.register(URL)
admin.site.register(Contributor)
admin.site.register(ProductionCompany)
