from django.shortcuts import render
from blog.forms import AddAuthorForm, BlogEntryForm

# Create your views here.


#These three defs are for LIST pages, with ALL the albums, producers, or artists
def test(request):
    author_form = AddAuthorForm
    entry_form = BlogEntryForm
    return render(request, 'blog/temp.html', {'author_form': author_form, 'entry_form': entry_form})
