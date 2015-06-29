from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weird_canada.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'indie_db.views.index'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', 'blog.views.test', name="test_page"),
    url(r'^wc_admin/$', 'blog.views.wc_admin_hub', name="wc_admin_hub_view"),

    # profile / admin stuff

    url(r'^wc_admin/edit_profile/', 'blog.views.edit_profile', name="edit_profile_view"),
    url(r'^wc_admin/save_profile/', 'blog.views.save_profile', name="save_profile_view"),
    url(r'^wc_admin/write_profile/', 'blog.views.write_author_profile', name="write_author_profile_view"),
    url(r'^wc_admin/save_new_author/', 'blog.views.save_new_author_profile', name="save_new_author_profile_view"),

    # add stuff to the database

    url(r'^wc_admin/write_new_artist/', 'blog.views.write_new_artist', name="write_new_artist_view"),
    url(r'^wc_admin/write_new_work/', 'blog.views.write_new_work', name="write_new_work_view"),
    url(r'^wc_admin/save_new_artist/', 'blog.views.save_new_artist', name="save_new_artist_view"),
    url(r'^wc_admin/save_new_work/', 'blog.views.save_new_work', name="save_new_work_view"),
    url(r'^wc_admin/write_review/', 'blog.views.write_new_review_article', name="write_new_review_article_view"),
    url(r'^wc_admin/write_mono_article/', 'blog.views.write_new_mono_article', name="write_new_mono_article_view"),
    url(r'^wc_admin/save_mono_article/', 'blog.views.save_new_mono_article', name="save_new_mono_article_view"),
    url(r'^wc_admin/save_review/', 'blog.views.save_new_review_article', name="save_new_review_article_view"),
    url(r'^wc_admin/add_contributor/', 'blog.views.add_contributor', name="add_contributor_view"),
    url(r'^wc_admin/add_production_company/', 'blog.views.add_production_company', name="add_production_company_view"),
    url(r'^wc_admin/write_tracklist/', 'blog.views.write_tracklist', name="add_tracklist_view"),
    url(r'^wc_admin/save_tracklist/', 'blog.views.save_tracklist', name="save_tracklist_view"),
    url(r'^wc_admin/write_new_production_company/', 'blog.views.write_new_production_company', name="add_new_production_company_view"),
    url(r'^wc_admin/save_new_production_company/', 'blog.views.save_new_production_company', name="save_new_production_company_view"),

    # view raw database info

    url(r'^wc_admin/view_artist/$', 'blog.views.view_artist', name="view_artist_view"),
    url(r'^wc_admin/view_work/$', 'blog.views.view_work', name="view_work_view"),
    url(r'^wc_admin/view_article/$', 'blog.views.view_article', name="view_article_view"),
    url(r'^wc_admin/view_production_company/$', 'blog.views.view_production_company', name="view_production_company_view"),
    url(r'^wc_admin/browse_articles/$', 'blog.views.browse_articles', name="browse_articles_view"),
    url(r'^wc_admin/browse_artists/$', 'blog.views.browse_artists', name="browse_artists_view"),
    url(r'^wc_admin/browse_works/$', 'blog.views.browse_works', name="browse_works_view"),

    # The Front Site

    url(r'^article/$', 'indie_db.views.article', name="front_article_view"),
    url(r'^search/$', 'indie_db.views.search_articles', name="search_articles_view"),

    # Front / Indie_DB

    url(r'^indie_db/$', 'blog.views.indie_index', name="indie_index_page"),
    url(r'^indie_db/works/search/$', 'indie_db.views.search_works', name="search_works_view"),
    url(r'^indie_db/works/$', 'indie_db.views.single_work', name="single_work_view"),
    url(r'^indie_db/artists/search/$', 'indie_db.views.search_artists', name="search_artists_view"),
    url(r'^indie_db/artists/$', 'indie_db.views.single_artist', name="single_artist_view"),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

