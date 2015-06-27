# Django core stuff
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Weird Canada apps stuff
from indie_db.forms import AddArtistForm, AddWorkForm, AddProductionCompanyForm
from indie_db.models import Artist, Work, URL, Style, Contributor, Track, ProductionCompany
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
    if request.method == 'GET' and 'cat' in request.GET:        
        category = request.GET.get('category')
        articles = Article.objects.filter(publish=True).filter(article_category__title__contains=category).order_by('-date_created')
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

    if page == 1 or request.GET.get('page') == 1:
        return render(request, 'front/front_page.html', {'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page})
    else:
        return render(request, 'front/grid_page.html', {'categories': categories, 'articles': articles, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page})


