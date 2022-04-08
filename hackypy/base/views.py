from django.shortcuts import render, redirect
from .utils import  newsData1
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def storyView(request):

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
       'posts':page_obj
    }
    return render(request, 'base/home.jinja', context)


@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.by = request.user
            post.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/post_form.jinja', context)


@login_required(login_url='login')
def createComments(request, pk):
    comments = Comment.objects.filter(post__id=pk)
    post = Post.objects.get(id=pk)
    form = CommentForm()
    

    if request.method == 'POST':
        comment = Comment.objects.create(
            creator = request.user,
            by = request.user,
            post = post,
            text = request.POST.get('text')
        )
        return redirect('create-comments', pk=post.id)

    context = {'form':form,'comments':comments, 'post':post}
    return render(request, 'base/comments_form.jinja', context)


@login_required(login_url='login')
def replyComment(request, pk):
    comment = Comment.objects.get(id=pk)
    post = comment.post
    form = CommentForm()
    if request.method == 'POST':
        reply = Comment.objects.create(
            creator = request.user,
            by = request.user,
            parent = comment,
            post = post,
            text = request.POST.get('text')
        )
        return redirect('create-comments', pk=post.id)

    context = {'form':form, 'comment':comment}
    return render(request, 'base/reply_form.jinja', context)


@login_required(login_url='login')
def postVote(request, pk):
    post = Post.objects.get(id=pk)

    if post.upVotes.filter(id=request.user.id).exists():
        post.upVotes.remove(request.user)
    else:
        post.upVotes.add(request.user)
    
    return redirect('home')


def searchPost(request):
    q = q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(Q(title__icontains=q))

    context = { 'posts' : posts}
    return render(request, 'base/search_result.jinja', context)