from django.shortcuts import render
from blog.forms import AddAuthorForm

# Create your views here.


#These three defs are for LIST pages, with ALL the albums, producers, or artists
def test(request):
    author_form = AddAuthorForm
    return render(request, 'blog/temp.html', {'author_form': author_form})
