from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('posts:list')

    context = {
        'form': form,
        'title': 'Login'
    }
    return render(request, 'posts/form.html', context=context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        # In lecture video, this login needs to authenticate first
        # But for me, login is works fine 
        # new_user = authenticate(username=user.username, password=password)
        # login(request, new_user)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/posts')

    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'posts/form.html', context=context)
    
def logout_view(request):
    logout(request)
    return redirect('/posts')