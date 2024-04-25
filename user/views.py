from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout

# Create your views here.
@login_required
def LogoutView(request):
    logout(request)
    return redirect(reverse('post-list'))
