from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Article


class LatestArticlesFeed(Feed):
    title = "Weird Canada Latest Articles"
    link = "/feed/"
    description = "The latest articles from WeirdCanada.com"

    def items(self):
        return Article.objects.order_by('-date_created')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        body_en = item.body_en[:700]
        body_fr = item.body_fr[:700]
        summary = '<b>EN:</b><br>' + body_en + '<br><br><b>FR:</b><br>' + body_fr
        return summary

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return "/article/?id=" + str(item.id)
