from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse

from App_Login.models import Follow, UserProfile
from App_Posts.forms import CommentForm, PostForm
from App_Posts.models import Comment, Like, Post

# Create your views here.

@login_required
def home(request):
    search = ''
    result = User.objects.none()

    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        post_id = request.POST.get('post_id')
        if comment_form.is_valid() and post_id:
            post = Post.objects.get(id=post_id)
            Comment.objects.create(
                post=post,
                user=request.user,
                content=comment_form.cleaned_data['content']
            )
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)

    return render(request, 'App_Posts/home.html', {
        'title': 'Home',
        'search': search,
        'result': result,
        'posts': posts,
        'liked_post_list': liked_post_list,
        'comment_form': comment_form
    })


@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'App_Login/user.html', {'post': post})
