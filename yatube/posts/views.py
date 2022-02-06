from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from posts.forms import PostForm

NUMBER_POSTS = 10


def index(request):
    title = 'Последние обновления на сайте'
    post_list = Post.objects.select_related('group').all()
    paginator = Paginator(post_list, NUMBER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, NUMBER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    title = username + ' профайл пользователя'
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, NUMBER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_number = posts.count()
    context = {
        'post_number': post_number,
        'page_obj': page_obj,
        'author': user,
        'title': title,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    get_user_object = User.objects.get(id=post.author_id)
    user = get_user_object.username
    post_list = Post.objects.filter(author=get_user_object)
    posts_count = post_list.count()
    context = {
        'username': user,
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template_name = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        username = post.author.username
        return redirect('posts:profile', username)
    return render(request, template_name, {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.user == post.author and request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form = PostForm(instance=post)
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {
        'form': form, 'post': post, 'is_edit': True, })
