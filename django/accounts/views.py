from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_vaild():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)