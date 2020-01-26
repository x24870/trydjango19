from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render

from .forms import UserLoginForm

def login_view(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data('username')
        password = form.cleaned_data('password')

    context = {
        'form': form,
        'title': 'Login'
    }
    return render(request, 'posts/form.html', context=context)

def register_view(request):
    return render(request, 'form.html', {})
    
def logout_view(request):
    return render(request, 'form.html', {})