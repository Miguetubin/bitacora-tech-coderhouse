from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
from .models import Post


def post_list(request):
    query = request.GET.get('q', '').strip()[:200]
    posts = Post.objects.select_related('author')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    page = Paginator(posts, 6).get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {
        'page_obj': page, 'query': query,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Tu publicación ya está disponible.')
        return redirect(post)
    return render(request, 'blog/post_form.html', {'form': form, 'editing': False})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST if request.method == 'POST' else None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Los cambios se guardaron.')
        return redirect(post)
    return render(request, 'blog/post_form.html', {'form': form, 'editing': True, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'La publicación fue eliminada.')
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def about(request):
    return render(request, 'blog/about.html')
