from django.shortcuts import render

# Create your views here.


#These three defs are for LIST pages, with ALL the albums, producers, or artists
def test(request):
    return render(request, 'blog/temp.html', {})
