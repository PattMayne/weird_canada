from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Article


class LatestArticlesFeed(Feed):
    title = "Weird Canada Latest Articles"
    link = "/"
    description = "The latest articles from WeirdCanada.com"

    def articles(self):
        return Article.objects.order_by('-date_created')[:5]

    def article_title(self, article):
        return article.title

    def item_description(self, article):
        return article.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, article):
        return reverse('news-item', args=[article.pk])