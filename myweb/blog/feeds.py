import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


# creamos la clase para mostrar los ultimos post en formato rss
class LatestPostsFeed(Feed):
    title = 'Mi blog'
    link = reverse_lazy('blog:post_list')
    description = 'Nuevos posts de mi blog.'

    def items(self):
        return Post.published.all()[:5] # solo los 5 primeros post

    def item_title(self, item): # metodo que devuelve el titulo del item
        return item.title

    def item_description(self, item): # metodo que devuelve la descripcion del item
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item): # metodo que devuelve la fecha de publicacion del item
        return item.publish
    
    
