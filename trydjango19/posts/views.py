from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import PostForm
from .models import Post

def post_list(request):
    all_post_list = Post.objects.all()
    paginator = Paginator(all_post_list, 5) #show 5 posts per page
    page_req_var = 'page'
    page = request.GET.get(page_req_var)
    context = {
        'title': 'Post lists',
        'page_req_var': page_req_var,
        'post_list': paginator.get_page(page)
    }
    return render(request, 'posts/post_list.html', context=context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'create post succesfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form
    }
    return render(request, 'posts/post_form.html', context)

def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', {'instance': instance})

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Update post succesfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'posts/post_form.html', context)

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'delete post succesfully')
    return redirect('posts:list')