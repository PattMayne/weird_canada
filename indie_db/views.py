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
from blog.models import Article, Author, Tag, ArticleCategory
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

    articles_per_page = 12
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
    articles = Article.objects.filter(publish=True)
    search_string = '&'

    if request.method == 'GET':

        if 'title' in request.GET and request.GET.get('title') != '':
            search_string += 'title=' + request.GET.get('title') + '&'
            articles = articles.filter(title__icontains=request.GET.get('title'))

        if 'artist_name' in request.GET and request.GET.get('artist_name') != '':
            search_string += 'artist_name=' + request.GET.get('artist_name') + '&'
            articles = articles.filter(work_link__creator__name__icontains=request.GET.get('artist_name'))

        if 'tag' in request.GET and request.GET.get('tag') != '':
            search_string += 'tag=' + request.GET.get('tag') + '&'
            articles = articles.filter(tags__tag_name=request.GET.get('tag'))

        if 'cat' in request.GET and request.GET.get('cat') != '' and request.GET.get('cat') != 'all':
            search_string += 'cat=' + request.GET.get('cat') + '&'
            articles = articles.filter(article_category__title__icontains=request.GET.get('cat'))

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
    return render(request, 'front/search_articles.html', {'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string})


# INDIE_DB stuff

def search_works(request):
    works = Work.objects.all()
    works_per_page = 3
    categories = WorkCategory.objects.all()
    works = Work.objects.filter()
    search_string = '&'

    if request.method == 'GET':

        if 'title' in request.GET and request.GET.get('title') != '':
            search_string += 'title=' + request.GET.get('title') + '&'
            works = works.filter(title__icontains=request.GET.get('title'))

        if 'artist_name' in request.GET and request.GET.get('artist_name') != '':
            search_string += 'artist_name=' + request.GET.get('artist_name') + '&'
            works = works.filter(creator__name__icontains=request.GET.get('artist_name'))

        if 'style' in request.GET and request.GET.get('style') != '':
            search_string += 'style=' + request.GET.get('style') + '&'
            works = works.filter(styles__name__icontains=request.GET.get('style'))

        if 'city' in request.GET and request.GET.get('city') != '':
            search_string += 'city=' + request.GET.get('city') + '&'
            works = works.filter(city__icontains=request.GET.get('city'))

        if 'cat' in request.GET and request.GET.get('cat') != '' and request.GET.get('cat') != 'all':
            search_string += 'cat=' + request.GET.get('cat') + '&'
            works = works.filter(work_category__title__icontains=request.GET.get('cat'))

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

    return render(request, 'front/search_works.html', {'categories': categories, 'works': works, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search_string': search_string})


def single_work(request):
    if request.method == 'GET' and 'id' in request.GET:
        work_id = int(request.GET.get('id'))
        work = Work.objects.get(pk=work_id)
        return render(request, 'front/single_work.html', {'work': work})
    return HttpResponseRedirect('/indie_db/works/search/')


def single_artist(request):
    if request.method == 'GET':
        artist_id = request.GET.get('artist_id')
        artist = Artist.objects.get(pk=artist_id)
        return render(request, 'front/single_artist.html', {'artist': artist})


def single_publisher(request):
    if request.method == 'GET':
        publisher_id = request.GET.get('publisher_id')
        publisher = ProductionCompany.objects.get(pk=publisher_id)
        return render(request, 'front/single_publisher.html', {'publisher': publisher})
