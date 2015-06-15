# Django core stuff
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Weird Canada apps stuff
from indie_db.forms import AddArtistForm, AddWorkForm
from indie_db.models import Artist, Work, URL, Style
from blog.models import Article, Author, Tag
from blog.forms import AddArticleForm, AddAuthorForm, UpdateProfileForm, EditAuthorForm

# Create your views here.


#  EXTRA FUNCTIONS


def user_has_author(sent_user):
    this_user = sent_user
    author_profiles = Author.objects.filter(user_id=this_user.id)
    if len(author_profiles) > 0:
        return True
    else:
        return False


#TEST
def test(request):
    author_form = AddAuthorForm
    article_form = AddArticleForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'article_form': article_form, 'work_form': work_form, 'artist_form': artist_form})


# WC_ADMIN


def wc_admin_hub(request):
    if request.user.is_authenticated():
        if user_has_author(request.user):
            author = Author.objects.filter(user=request.user)[0]
            latest_articles = Article.objects.all().order_by('-id')[:5]
            latest_works = Work.objects.all().order_by('-id')[:5]
            latest_artists = Artist.objects.all().order_by('-id')[:5]

            total_authors = Author.objects.count()
            total_articles = Article.objects.count()
            total_works = Work.objects.count()
            total_artists = Artist.objects.count()

            args = {'author': author, 'latest_articles': latest_articles, 'latest_artists': latest_artists, 'latest_works': latest_works, 'total_articles': total_articles, 'total_artists': total_artists, 'total_authors': total_authors, 'total_works': total_works}
            return render(request, 'blog/wc_admin_hub.html', args)
        else:
            error_message = 'You must create an Author Profile before you can use this page.'
            return render(request, 'blog/error.html', {'error_message': error_message})
    else:
        error_message = 'You must log in before you can use this page.'
        return render(request, 'blog/error.html', {'error_message': error_message})


# Add Article to BLOG

def write_new_review_article(request):
    if request.method == 'POST' and 'work_id' in request.POST:
        work_id = request.POST.get('work_id')
        article_form = AddArticleForm
        return render(request, 'blog/article_review_write_new.html', {'article_form': article_form, 'work_id': work_id})
    else:
        error_message = 'Not enough info was passed to this page. <br> You should follow the procedure of finding a "work of art" listing, and writing an article based on that work of art by following the link in the listing.'
        return render(request, 'blog/error.html', {'error_message': error_message})


def save_new_review_article(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = AddArticleForm(request.POST)
        work_id = request.POST.get('work_id')
        work = Work.objects.get(pk=work_id)
        artist = work.creator
        if form.is_valid():
            article = form.save()
            author = Author.objects.filter(user=request.user)[0]
            article.author = author
            article.work_link = work
            article.artist_link = artist
            article.save()
            tags_string = request.POST.get('tags')
            tags_list = tags_string.split(',')
            tags = []

            for tag in tags_list:
                tags.append(tag.strip().lower())

            # A Tag is another model, linked to the "article" via a ManyToMany field
            # Here we check to see if the user has entered tags that already exist in the database
            for tag in tags:
                pre_existing_tags = Tag.objects.filter(tag_name=tag)
                if len(pre_existing_tags) > 0:
                    pre_existing_tag = pre_existing_tags[0]
                    article.tags.add(pre_existing_tag)
                    article.save()
                else:
                    #create a new tag, save it to the DB, and add it to the article
                    new_tag = Tag()
                    new_tag.tag_name = tag
                    new_tag.save()
                    article.tags.add(new_tag)
                    article.save()
            return HttpResponseRedirect('/indie_db/view_article/?id=' + str(article.id))
        else:
            error_message = 'The form was not valid. The data was not saved.'
            return render(request, 'blog/error.html', {'error_message': error_message, 'form': form})
    else:
        error_message = 'The info was not properly posted. The data was not saved.'
        return render(request, 'blog/error.html', {'error_message': error_message})


def view_article(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            article = Article.objects.get(pk=request.GET.get('id'))
            return render(request, 'blog/article_view.html', {'article': article})


# Add Info to INDIE_DB (maybe later move to the indie_db views.py file)

def write_new_artist(request):
    artist_form = AddArtistForm
    return render(request, 'blog/artist_write_new.html', {'artist_form': artist_form})


def save_new_artist(request):
    if request.method == 'POST':
        form = AddArtistForm(request.POST)
        artist = None
        if form.is_valid():
            artist = form.save()
            artist_id = artist.id
            if 'website_name' in request.POST and 'website_url' in request.POST:
                website_name = request.POST.get('website_name')
                website_url = request.POST.get('website_url')
                website = URL()
                website.name = website_name
                website.link = website_url
                website.save()

                artist.website = website
                artist.save()
            return HttpResponseRedirect('/indie_db/view_artist/?id=' + str(artist_id))
        else:
            error_message = 'The form was not valid. The data was not saved.'
            return render(request, 'blog/error.html', {'error_message': error_message, 'form': form})


def write_new_work(request):
    if request.method == 'POST':
        if'artist_id' in request.POST:
            artist_id = request.POST.get('artist_id')
            work_form = AddWorkForm
            return render(request, 'blog/work_write_new.html', {'work_form': work_form, 'artist_id': artist_id})


def save_new_work(request):
    if request.method == 'POST' and 'artist_id' in request.POST:
        form = AddWorkForm(request.POST)
        artist_id = request.POST.get('artist_id')
        artist = Artist.objects.get(pk=artist_id)
        work = None
        if form.is_valid():
            work = form.save()
            work.creator = artist
            work.save()
            work_id = work.id
            if 'website_name' in request.POST and 'website_url' in request.POST:
                website_name = request.POST.get('website_name')
                website_url = request.POST.get('website_url')
                website = URL()
                website.name = website_name
                website.link = website_url
                website.save()

                work.website = website
                work.save()
            if 'styles' in request.POST:
                styles_string = request.POST.get('styles')
                styles_list = styles_string.split(',')
                styles = []

                for style in styles_list:
                    styles.append(style.strip().lower())

                # A Style is another model, linked to the "work" via a ManyToMany field
                # Here we check to see if the user has entered styles that already exist in the database
                for style in styles:
                    pre_existing_styles = Style.objects.filter(name=style)
                    if len(pre_existing_styles) > 0:
                        pre_existing_style = pre_existing_styles[0]
                        work.styles.add(pre_existing_style)
                        work.save()
                    else:
                        #create a new style, save it to the DB, and add it to the work
                        new_style = Style()
                        new_style.name = style
                        new_style.save()
                        work.styles.add(new_style)
                        work.save()

            return HttpResponseRedirect('/indie_db/view_work/?id=' + str(work_id))
        else:
            error_message = 'The form was not valid. The data was not saved.'
            return render(request, 'blog/error.html', {'error_message': error_message, 'form': form})
    else:
        error_message = 'The info was not properly posted. The data was not saved.'
        return render(request, 'blog/error.html', {'error_message': error_message})


# View raw data from indie_db

def view_artist(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            artist_id = request.GET.get('id')
            artist = Artist.objects.get(pk=artist_id)
            works = Work.objects.filter(creator=artist)
            return render(request, 'blog/artist_view.html', {'artist': artist, 'works': works})


def view_work(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            work = Work.objects.get(pk=request.GET.get('id'))
            articles = Article.objects.filter(work_link=work)
            return render(request, 'blog/work_view.html', {'work': work, 'articles': articles})


def browse_articles(request):
    results_per_page = 18
    search_request = ''
    order_by_request = ''
    order_by = '-id'
    if request.method == 'GET':
        
        order_by_request = request.GET.get('order_by')
        search_request = request.GET.get('search')

        if search_request is None:
            search_request = ''
        
        if order_by_request == 'date_desc':
            order_by = '-date_created'
        elif order_by_request == 'date_asc':
            order_by = 'date_created'
        elif order_by_request == 'title_asc':
            order_by = 'title'
        elif order_by_request == 'title_desc':
            order_by = '-title'

        all_articles = Article.objects.filter(title__icontains=search_request).order_by(order_by)
    else:
        all_articles = Article.objects.all().order_by('-id')

    pager = Paginator(all_articles, results_per_page)

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
    return render(request, 'blog/browse_articles.html', {'articles': articles, 'results_per_page': results_per_page, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search': search_request, 'order_by': order_by_request})


def browse_artists(request):
    results_per_page = 18
    search_request = ''
    order_by_request = ''
    order_by = '-id'
    if request.method == 'GET':
        
        order_by_request = request.GET.get('order_by')
        search_request = request.GET.get('search')

        if search_request is None:
            search_request = ''
        
        elif order_by_request == 'name_asc':
            order_by = 'name'
        elif order_by_request == 'name_desc':
            order_by = '-name'
        elif order_by_request == 'birthdate_asc':
            order_by = 'birthdate'
        elif order_by_request == 'birthdate_desc':
            order_by = '-birthdate'

        all_artists = Artist.objects.filter(name__icontains=search_request).order_by(order_by)
    else:
        all_artists = Artist.objects.all().order_by('-id')

    pager = Paginator(all_artists, results_per_page)

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
    return render(request, 'blog/browse_artists.html', {'artists': artists, 'results_per_page': results_per_page, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search': search_request, 'order_by': order_by_request})


def browse_works(request):
    results_per_page = 18
    search_request = ''
    order_by_request = ''
    order_by = '-id'
    category = 'all'
    specific_category = False
    if request.method == 'GET':
        
        order_by_request = request.GET.get('order_by')
        search_request = request.GET.get('search')

        if search_request is None:
            search_request = ''
        
        elif order_by_request == 'title_asc':
            order_by = 'title'
        elif order_by_request == 'title_desc':
            order_by = '-title'
        elif order_by_request == 'created_asc':
            order_by = 'created'
        elif order_by_request == 'created_desc':
            order_by = '-created'

        if 'category' in request.GET:
            category = request.GET.get('category')
            if category != 'all':
                specific_category = True

        if specific_category:
            all_works = Work.objects.filter(category=category).filter(title__icontains=search_request).order_by(order_by)
        else:
            all_works = Work.objects.filter(title__icontains=search_request).order_by(order_by)
    else:
        all_works = Work.objects.all().order_by('-id')

    pager = Paginator(all_works, results_per_page)

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
    return render(request, 'blog/browse_works.html', {'works': works, 'results_per_page': results_per_page, 'total_results': pager.count, 'number_of_pages': pager.num_pages, 'page': page, 'search': search_request, 'order_by': order_by_request, 'category': category})


# WC_ADMIN profile stuff


def edit_profile(request):
    if request.user.is_authenticated:
        if user_has_author(request.user):
            author_profile = Author.objects.filter(user=request.user)[0]
            author_form = EditAuthorForm(instance=author_profile)
            user_form = UpdateProfileForm(instance=request.user)

            return render(request, 'blog/edit_profile.html', {'author_form': author_form, 'user_form': user_form})
        else:
            error_message = 'You must have an author account to access this page.'
            return render(request, 'blog/error.html', {'error_message': error_message})
    else:
        error_message = 'You must be logged in to access this page.'
        return render(request, 'blog/error.html', {'error_message': error_message})


def save_profile(request):
    if request.user.is_authenticated:
        if user_has_author(request.user):
            author_profile = Author.objects.filter(user=request.user)[0]
            author_form = EditAuthorForm(request.POST, instance=author_profile)
            user_form = UpdateProfileForm(request.POST, instance=request.user)
            if author_form.is_valid():
                author_form.save()
            if user_form.is_valid():
                user_form.save()
            if 'password' in request.POST:
                if request.POST.get('password') != '':
                    request.user.set_password(request.POST.get('password'))
                    request.user.save()
            return HttpResponseRedirect('/wc_admin/')
    error_message = 'This page does not exist. So how are you here??'
    return render(request, 'blog/error.html', {'error_message': error_message})
