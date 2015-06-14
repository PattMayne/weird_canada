from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weird_canada.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', 'blog.views.test', name="test_page"),
    url(r'^wc_admin/', 'blog.views.wc_admin_hub', name="wc_admin_hub_view"),
    # add stuff to the database
    url(r'^wc_admin/write_new_artist/$', 'blog.views.write_new_artist', name="write_new_artist_view"),
    url(r'^wc_admin/write_new_work/$', 'blog.views.write_new_work', name="write_new_work_view"),
    url(r'^wc_admin/save_new_artist/$', 'blog.views.save_new_artist', name="save_new_artist_view"),
    url(r'^wc_admin/save_new_work/$', 'blog.views.save_new_work', name="save_new_work_view"),
    url(r'^wc_admin/write_review/$', 'blog.views.write_new_review_article', name="write_new_review_article"),
    url(r'^wc_admin/save_review/$', 'blog.views.save_new_review_article', name="save_new_review_article_view"),

    # view raw database info
    url(r'^indie_db/view_artist/$', 'blog.views.view_artist', name="view_artist_view"),
    url(r'^indie_db/view_work/$', 'blog.views.view_work', name="view_work_view"),
    url(r'^indie_db/view_article/$', 'blog.views.view_article', name="view_article_view"),
    url(r'^indie_db/browse_articles/$', 'blog.views.browse_articles', name="browse_articles_view"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
