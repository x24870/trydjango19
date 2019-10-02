from django.http import HttpResponse 
from django.shortcuts import render, get_object_or_404

from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_create(request):
    return HttpResponse("<h1>Retrun from post_create</h1>")

def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_update(request):
    return HttpResponse("<h1>Retrun from post_upadte</h1>")

def post_delete(request):
    return HttpResponse("<h1>Retrun from post_delete</h1>")

