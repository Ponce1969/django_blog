"""
Configuración de URL para el proyecto myweb.

La lista `urlpatterns` dirige las URL a las vistas. Para obtener más información, consulte:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Ejemplos:
Vistas de funciones
    1. Agregue una importación: desde las vistas de importación de my_app
    2. Agregue una URL a urlpatterns: ruta('', views.home, nombre='home')
Vistas basadas en clases
    1. Agregue una importación: desde other_app.views import Inicio
    2. Agregue una URL a urlpatterns: ruta('', Home.as_view(), nombre='home')
Incluyendo otra URLconf
    1. Importe la función include(): desde django.urls importe include, ruta
    2. Agregue una URL a urlpatterns: ruta('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap




sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')


     
]   


