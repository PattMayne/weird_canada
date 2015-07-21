# Django core stuff
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Weird Canada apps stuff
from indie_db.forms import AddArtistForm, AddWorkForm, AddProductionCompanyForm
from indie_db.models import Artist, Work, URL, Style, Contributor, Track, ProductionCompany, WorkCategory
from blog.models import Article, Author, Tag, ArticleCategory, HowCategory, Page
from blog.forms import AddArticleForm, AddAuthorForm, UpdateProfileForm, EditAuthorForm


# Create your views here.

# TODO:
#       ARTICLES:
#
#       -Show 12 articles for 'Front Page' for each category
#       -Show sub-pages for pag2++ for each category
#       -Show search results
#       -Show single article
#
#       -front_page.html
#       -grid_page.html
#       -article.html
#
#
#       INDIE_DB
# 
#       -Very simple grid of 20 'Works' which can be searched, sorted, and browsed by category, title, date, styles/genres, etc
#       -Very simple list of 30 'Artists' which can be searched, browsed, and sorted by name, etc...
#       -Display single Artist
#       -Display single Work
#
#       -works.html
#       -artists.html
#       -work_single.html
#       -artist_single.html
#


'''
        Here's the big front page.
        This will show the actual front page for all categories of post,
        but it will also show the front page for each individual category.

        This view will also load sub-pages which lack the big splash image and just show a grid of articles to display.
        That will be for page2++
'''


def index(request):

    articles_per_page = 9
    category = 'all'

    articles = []
    categories = ArticleCategory.objects.all()
    if request.method == 'GET' and 'cat' in request.GET and request.GET.get('cat') != 'all':
        category = request.GET.get('cat')
        articles = Article.objects.filter(publish=True).filter(article_category__title__icontains=category).order_by('-date_created')
    else:
        articles = Article.objects.filter(publish=True).order_by('-date_created')

    pager = Paginator(articles, articles_per_page)

    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        articles = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = pager.page(pager.num_pages)

    if page == 1 or page == '1':
        return render(request, 'front/front_page.html', {'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'cat': category})
    else:
        return render(request, 'front/grid_page.html', {'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'cat': category})


def article(request):
    if request.method == 'GET' and 'id' in request.GET:
        categories = ArticleCategory.objects.all()
        article_id = request.GET.get('id')
        article = Article.objects.get(pk=article_id)
        return render(request, 'front/article.html', {'categories': categories, 'article': article})


def search_articles(request):
    articles_per_page = 12
    categories = ArticleCategory.objects.all()
    how_categories = HowCategory.objects.all()
    articles = Article.objects.filter(publish=True)
    search_string = '&'
    search_display = []

    if request.method == 'GET':

        if 'title' in request.GET and request.GET.get('title') != '':
            search_string += 'title=' + request.GET.get('title') + '&'
            search_display.append(request.GET.get('title'))
            articles = articles.filter(title__icontains=request.GET.get('title'))

        if 'artist_name' in request.GET and request.GET.get('artist_name') != '':
            search_string += 'artist_name=' + request.GET.get('artist_name') + '&'
            search_display.append(request.GET.get('artist_name'))
            articles = articles.filter(work_link__creator__name__icontains=request.GET.get('artist_name'))

        if 'tag' in request.GET and request.GET.get('tag') != '':
            search_string += 'tag=' + request.GET.get('tag') + '&'
            search_display.append(request.GET.get('tag'))
            articles = articles.filter(tags__tag_name=request.GET.get('tag'))

        if 'cat' in request.GET and request.GET.get('cat') != '' and request.GET.get('cat') != 'all':
            search_string += 'cat=' + request.GET.get('cat') + '&'
            search_display.append(request.GET.get('cat'))
            articles = articles.filter(article_category__title__icontains=request.GET.get('cat'))

        if 'how' in request.GET and request.GET.get('how') != '' and request.GET.get('how') != 'all':
            search_string += 'cat=' + request.GET.get('how') + '&'
            search_display.append(request.GET.get('how'))
            articles = articles.filter(how_category__title__icontains=request.GET.get('how'))

    articles = articles.order_by('-date_created')

    pager = Paginator(articles, articles_per_page)

    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        articles = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = pager.page(pager.num_pages)
    return render(request, 'front/search_articles.html', {'how_categories': how_categories, 'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string, 'search_display': search_display})


# INDIE_DB stuff

def indie_index(request):
    categories = ArticleCategory.objects.all()
    work_categories = WorkCategory.objects.all()
    return render(request, 'front/indie_db.html', {'categories': categories, 'work_categories': work_categories})


def search_works(request):
    works = Work.objects.all()
    works_per_page = 3
    categories = ArticleCategory.objects.all()
    work_categories = WorkCategory.objects.all()
    search_string = '&'
    search_display = []

    if request.method == 'GET':

        if 'title' in request.GET and request.GET.get('title') != '':
            search_display.append(request.GET.get('title'))
            search_string += 'title=' + request.GET.get('title') + '&'
            works = works.filter(title__icontains=request.GET.get('title'))

        if 'artist_name' in request.GET and request.GET.get('artist_name') != '':
            search_display.append(request.GET.get('artist_name'))
            search_string += 'artist_name=' + request.GET.get('artist_name') + '&'
            works = works.filter(creator__name__icontains=request.GET.get('artist_name'))

        if 'style' in request.GET and request.GET.get('style') != '':
            search_display.append(request.GET.get('style'))
            search_string += 'style=' + request.GET.get('style') + '&'
            works = works.filter(styles__name__icontains=request.GET.get('style'))

        if 'city' in request.GET and request.GET.get('city') != '':
            search_display.append(request.GET.get('city'))
            search_string += 'city=' + request.GET.get('city') + '&'
            works = works.filter(city__icontains=request.GET.get('city'))

        if 'cat' in request.GET and request.GET.get('cat') != '' and request.GET.get('cat') != 'all':
            search_display.append(request.GET.get('cat'))
            search_string += 'cat=' + request.GET.get('cat') + '&'
            works = works.filter(work_category__title__icontains=request.GET.get('cat'))

        if 'self_published' in request.GET:
            search_display.append('Self Published')
            search_string += 'self_published=' + 'True' + '&'
            works = works.filter(self_published=True)

    works = works.order_by('-created')

    pager = Paginator(works, works_per_page)

    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        works = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        works = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        works = pager.page(pager.num_pages)

    return render(request, 'front/search_works.html', {'work_categories': work_categories, 'categories': categories, 'works': works, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string, 'search_display': search_display})


def search_artists(request):
    artists = Artist.objects.all()
    artists_per_page = 3
    categories = ArticleCategory.objects.all()
    search_display = []
    search_string = '&'

    if request.method == 'GET':

        if 'name' in request.GET and request.GET.get('name') != '':
            search_display.append(request.GET.get('name'))
            search_string += 'name=' + request.GET.get('name') + '&'
            artists = artists.filter(name__icontains=request.GET.get('name'))

    #artists = artists.order_by('-birthdate')

    pager = Paginator(artists, artists_per_page)

    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        artists = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        artists = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        artists = pager.page(pager.num_pages)

    return render(request, 'front/search_artists.html', {'categories': categories, 'artists': artists, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string, 'search_display': search_display})


def search_publishers(request):
    publishers = ProductionCompany.objects.all()
    publishers_per_page = 3
    categories = ArticleCategory.objects.all()
    search_display = []
    search_string = '&'

    if request.method == 'GET':

        if 'name' in request.GET and request.GET.get('name') != '':
            search_display.append(request.GET.get('name'))
            search_string += 'name=' + request.GET.get('name') + '&'
            publishers = publishers.filter(name__icontains=request.GET.get('name'))

        if 'format' in request.GET and request.GET.get('format') != '':
            search_display.append(request.GET.get('format'))
            search_string += 'format=' + request.GET.get('format') + '&'
            publishers = publishers.filter(formats__label__icontains=request.GET.get('format'))

        if 'style' in request.GET and request.GET.get('style') != '':
            search_display.append(request.GET.get('style'))
            search_string += 'style=' + request.GET.get('style') + '&'
            publishers = publishers.filter(styles__name__icontains=request.GET.get('style'))

        if 'city' in request.GET and request.GET.get('city') != '':
            search_display.append(request.GET.get('city'))
            search_string += 'city=' + request.GET.get('city') + '&'
            publishers = publishers.filter(city__icontains=request.GET.get('city'))

    pager = Paginator(publishers, publishers_per_page)

    if request.method == 'GET' and 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    try:
        publishers = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        publishers = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        publishers = pager.page(pager.num_pages)

    return render(request, 'front/search_publishers.html', {'categories': categories, 'publishers': publishers, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string, 'search_display': search_display})


def single_work(request):
    categories = ArticleCategory.objects.all()
    articles = []
    if request.method == 'GET' and 'id' in request.GET:
        work_id = int(request.GET.get('id'))
        articles = Article.objects.filter(work_link=work_id)
        work = Work.objects.get(pk=work_id)
        return render(request, 'front/single_work.html', {'categories': categories, 'work': work, 'articles': articles})
    else:
        return HttpResponseRedirect('/indie_db/works/search/')


def single_artist(request):
    categories = ArticleCategory.objects.all()
    works = []
    if request.method == 'GET' and 'id' in request.GET:
        artist_id = request.GET.get('id')
        artist = Artist.objects.get(pk=artist_id)
        works = Work.objects.filter(creator=artist)
        styles = []
        for work in works:
            for style in work.styles.all():
                if style not in styles:
                    styles.append(style)

        return render(request, 'front/single_artist.html', {'categories': categories, 'artist': artist, 'styles': styles, 'works': works})
    else:
        return HttpResponseRedirect('/indie_db/artists/search/')


def single_publisher(request):
    categories = ArticleCategory.objects.all()
    if request.method == 'GET':
        publisher_id = request.GET.get('id')
        publisher = ProductionCompany.objects.get(pk=publisher_id)
        works = Work.objects.filter(production_company=publisher)
        return render(request, 'front/single_publisher.html', {'categories': categories, 'publisher': publisher, 'works': works})
    else:
        return HttpResponseRedirect('/indie_db/works/search/')


def view_page(request):
    if request.method == 'GET':
        page_handle = request.GET.get('page')
        page = Page.objects.filter(handle=page_handle)[0]
        body = page.body_en
