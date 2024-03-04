from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap): # clase que define un sitemap
    changefreq = 'weekly' # frecuencia de cambio semanal
    priority = 0.9 # prioridad de 0 a 1 la escalada de prioridad.
    def items(self): # metodo que devuelve los items del sitemap
        return Post.published.all() # todos los post publicados
    def lastmod(self, obj): # metodo que devuelve la fecha de modificacion
        return obj.updated
    