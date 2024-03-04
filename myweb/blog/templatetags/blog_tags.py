 # Aca se crean los tags personalizados para la aplicacion blog.
 
from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown


register = template.Library()
@register.simple_tag   # decorador que convierte la funcion en un tag personalizado
def total_posts():
    return Post.published.count() 

@register.inclusion_tag('blog/post/latest_posts.html') #con el decorador inclusion_tag se crea un tag que renderiza un template y retorna un diccionario de contexto.
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count] # obtener los ultimos 5 post ordenados por fecha de publicacion
    return {'latest_posts': latest_posts}



@register.filter(name='markdown') # con markdown se crea un filtro personalizado que convierte el texto en markdown
def markdown_format(text):
    return mark_safe(markdown.markdown(text)) # se usa la funcion mark_safe para marcar el texto como seguro y evitar que se escape el html