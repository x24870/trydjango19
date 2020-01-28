from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Comment
from .forms import CommentForm

# Create your views here.
def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)

    initial_data = {
        'content_type': comment.content_type,
        'object_id' : comment.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    print(form.errors)
    if form.is_valid() and request.user.is_authenticated:
        content_type = ContentType.objects.get(model=comment.__class__.__name__.lower())

        parent_obj = None
        parent_id = request.POST.get('parent_id')
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()

        obj_id = form.cleaned_data.get('object_id')
        content = form.cleaned_data.get('content')

        newComment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content,
            parent = parent_obj
        )

        return HttpResponseRedirect(comment.get_absolute_url())

    context = {
        'comment': comment,
        'form': form
    }
    return render(request, 'comments/comment_thread.html', context=context)

@login_required(login_url='accounts:login')# Or you can add LOGIN_URL parameter in settings.py
def confirm_delete(request, id):
    #comment = get_object_or_404(Comment, id=id)
    try:
        comment = Comment.objects.get(id=id)
    except:
        return Http404

    if request.user != comment.user:
        response = HttpResponse('You do not have permission to do this.')
        response.status_code = 403
        return response

    if request.method == 'POST':
        parent_obj_url = comment.content_object.get_absolute_url()
        # print(comment.id)
        # print(comment)
        # print(comment.content_type)
        # print(comment.content_object)
        # print(parent_obj_url)
        comment.delete()
        messages.success(request, 'Delete comment successfully')
        return HttpResponseRedirect(parent_obj_url)

    context = {
        'comment': comment
    }
    return render(request, 'comments/confirm_delete.html', context=context)