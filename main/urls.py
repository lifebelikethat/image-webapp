from django.urls import path
from . import views

urlpatterns = [
        path('posts/', views.PostList.as_view(), name='post-list'),
        path('posts/create/', views.PostCreate.as_view(), name='post-create'),
        path('posts/<int:id>/', views.PostDetail.as_view(), name='post-detail'),
        path('posts/<int:id>/update/', views.PostEdit.as_view(), name='post-update'),
        path('posts/<int:id>/delete/', views.PostDelete.as_view(), name='post-delete'),
        path('users/', views.UserList.as_view(), name='user-list'),
        path('users/<int:id>/', views.UserDetail.as_view(), name='user-detail'),
        path('tags/', views.TagList.as_view(), name='tag-list'),
        path('tags/create/', views.CreateTag.as_view(), name='tag-create'),
        path('tags/<int:id>/', views.UpdateTag.as_view(), name='tag-update'),
        path('tags/<int:id>/delete/', views.DeleteTag.as_view(), name='tag-delete'),
        ]
