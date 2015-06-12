from django.shortcuts import render
from blog.forms import AddAuthorForm, BlogEntryForm
from indie_db.forms import AddArtistForm, AddWorkForm
from indie_db.models import Artist, Work, URL

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
    return render(request, 'blog/write_new_artist.html', {'artist_form': artist_form})


def save_new_artist(request):
    if request.method == 'POST':
        form = AddArtistForm(request.POST)
        artist = None
        if form.is_valid():
            artist = form.save()
            if 'website_name' in request.POST and 'website_url' in request.POST:
                website_name = request.POST.get('website_name')
                website_url = request.POST.get('website_url')
                website = URL()
                website.name = website_name
                website.link = website_url
                website.save()
                
                artist.website = website
                artist.save()
            return render(request, 'blog/view_artist.html', {'artist': artist})
        else:
            error_message = 'The form was not valid. The data was not saved.'
            return render(request, 'blog/error.html', {'error_message': error_message, 'form': form})


# View raw data from indie_db

def view_artist(request):
    if request.method == 'POST':
        if 'artist' in request.POST:
            artist = Artist.objects.filter(name=request.POST.get('artist'))[0]
            return render(request, 'blog/view_artist.html', {'artist': artist})


def view_work(request):
    author_form = AddAuthorForm
    entry_form = BlogEntryForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'entry_form': entry_form, 'work_form': work_form, 'artist_form': artist_form})
