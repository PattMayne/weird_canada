# Django core stuff
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Weird Canada apps stuff
from blog.forms import AddAuthorForm, BlogEntryForm
from indie_db.forms import AddArtistForm, AddWorkForm
from indie_db.models import Artist, Work, URL, Style

# Create your views here.


#TEST
def test(request):
    author_form = AddAuthorForm
    entry_form = BlogEntryForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'entry_form': entry_form, 'work_form': work_form, 'artist_form': artist_form})


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
    work_form = AddWorkForm
    return render(request, 'blog/work_write_new.html', {'work_form': work_form})


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
                    styles.append(style.strip())

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
    error_message = 'The form was not valid. The data was not saved.'
    return render(request, 'blog/error.html', {'error_message': error_message, 'form': form})


# View raw data from indie_db

def view_artist(request):
    if request.method == 'GET':
        if 'id' in request.GET:
            artist = Artist.objects.get(pk=request.GET.get('id'))
            return render(request, 'blog/artist_view.html', {'artist': artist})


def view_work(request):
    author_form = AddAuthorForm
    entry_form = BlogEntryForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'entry_form': entry_form, 'work_form': work_form, 'artist_form': artist_form})
