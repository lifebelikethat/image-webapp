from django.urls import path, include
from . import views

urlpatterns = [
        path('logout/', views.LogoutView, name='logout'),
        path('', include('django.contrib.auth.urls')),
        ]
