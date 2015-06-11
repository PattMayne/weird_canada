from django.shortcuts import render
from blog.forms import AddAuthorForm, BlogEntryForm
from indie_db.forms import AddArtistForm, AddWorkForm

# Create your views here.


#These three defs are for LIST pages, with ALL the albums, producers, or artists
def test(request):
    author_form = AddAuthorForm
    entry_form = BlogEntryForm
    artist_form = AddArtistForm
    work_form = AddWorkForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'entry_form': entry_form, 'work_form': work_form, 'artist_form': artist_form})
