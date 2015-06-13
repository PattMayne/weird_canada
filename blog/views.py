# Django core stuff
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

# Weird Canada apps stuff
from indie_db.forms import AddArtistForm, AddWorkForm
from indie_db.models import Artist, Work, URL, Style
from blog.models import Article, Author, Tag
from blog.forms import AddArticleForm, AddAuthorForm

# Create your views here.


#TEST
def test(request):
    author_form = AddAuthorForm
    article_form = AddArticleForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'article_form': article_form, 'work_form': work_form, 'artist_form': artist_form})


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
            return render(request, 'blog/work_view.html', {'work': work})
