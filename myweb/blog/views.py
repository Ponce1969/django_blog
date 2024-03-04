from django.shortcuts import render
from .models import Post, Comment
from django.shortcuts import  render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

from django.views.decorators.http import require_POST  # decorador que permite que una vista solo responda a peticiones POST


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'




# Crear las vistas de la aplicacion blog
def post_list(request, tag_slug=None): # vista para ver la lista de post
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug) # obtener el tag por slug , retorna uno o un 404.
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 3) # 3 posts en cada pagina
    page_number = request.GET.get('page', 1)
    try:
         posts = paginator.page(page_number)
    except EmptyPage:
         posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
         posts = paginator.page(1)
    
    
    
    return render(request,
                 'blog/post/list.html',  # plantilla que se va a renderizar
                 {'posts': posts,       # contexto que se pasa a la plantilla
                    'tag': tag})           # variable de contexto que se pasa a la plantilla.
    
    
    
def post_share(request, post_id):# vista para compartir un post por correo
# obtener el post por id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED) # obtener el post por id
    sent = False
    if request.method == 'POST':
    # formulario enviado
       form = EmailPostForm(request.POST) # crear un formulario con los datos enviados
       if form.is_valid():
          # validacion de formulario
           cd = form.cleaned_data
           # mandar correo
           post_url = request.build_absolute_uri(post.get_absolute_url())   
           subject = f"{cd['name']} recommends you read {post.title}"         
           message = f"Read {post.title} at {post_url}\n\n" \
                     f"{cd['name']}\'s comments: {cd['comments']}"
           send_mail(subject, message, 'gompatri@gmail.com', [cd['to']])  # Mi correo      
           sent = True
           
                
    else:
        form = EmailPostForm()  # formulario vacio
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})   # contexto que se pasa a la plantilla
    
    
    
def post_detail(request, year, month, day, post): # vista para ver un post
    post = get_object_or_404(Post,
                              status=Post.Status.PUBLISHED, # solo se muestran los post publicados
                              slug=post,
                              publish__year=year,
                              publish__month=month,
                              publish__day=day)
    comments = post.comments.filter(active=True) # obtener los comentarios activos para este post 
    form = CommentForm() # formulario para agregar un comentario  
    post_tags_ids = post.tags.values_list('id', flat=True) # obtener los id de los tags del post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) # obtener de la clase Post los post que tengan los mismos tags que el post actual, excluye el propio post.
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] # con Count('tags') se cuenta el numero de tags que tienen en comun los post, se ordenan por el numero de tags en comun y por fecha de publicacion.
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts}) # contexto que se pasa a la plantilla
    
    
    
@require_POST  # decorador que permite que una vista solo responda a peticiones POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST) # crear un formulario con los datos enviados
    if form.is_valid():
        # Crear un objeto Comment pero no guardarlo en la base de datos todavía
        comment = form.save(commit=False)
         # Asignar el post actual al comentario
        comment.post = post
         # Salvar el comentario en la base de datos
        comment.save()
    return render(request, 'blog/post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})