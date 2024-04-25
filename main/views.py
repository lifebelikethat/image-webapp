from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Post, Tag, PostFeedBack
from .forms import PostEditForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
user_model = get_user_model()


class PostList(ListView):
    template_name = 'main/home.html'
    model = Post
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        if request.GET.get('tags'):
            tags = request.GET.get('tags').split(' ')

            if tags[-1] == '':
                tags = tags[:-1]

            if tags != ['']:
                queryset = None
                for tag in tags:
                    if queryset and tag != '':
                        queryset = queryset & self.model.objects.filter(tags__name=tag)

                    else:
                        queryset = self.model.objects.filter(tags__name=tag)
            else:
                queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.all()

        context = {
                self.context_object_name: queryset,
                }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    template_name = 'main/post-create.html'
    model = Post
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse_lazy('post-detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostEdit(UpdateView):
    template_name = 'main/post-update.html'
    pk_url_kwarg = 'id'
    form_class = PostEditForm
    model = Post

    def get_success_url(self):
        return reverse_lazy('post-detail', args=(self.object.id,))


class PostDelete(DeleteView):
    template_name = 'main/post-delete.html'
    model = Post
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('post-list')


class PostDetail(DetailView):
    template_name = 'main/post-detail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_instance = self.object
        tags = Tag.objects.filter(post=post_instance).order_by('-name')
        likes = len(post_instance.feedback.filter(feedback='L'))
        dislikes = len(post_instance.feedback.filter(feedback='D'))
        rating = likes - dislikes
        user = self.request.user
        user_rating = None

        if self.request.user.is_authenticated:
            if post_instance.id in list(user.feedback.all().values_list('post_id', flat=True)):
                if user.feedback.filter(post_id=post_instance.id):
                    user_rating = 'L'
                else:
                    user_rating = 'D'
            else:
                user_rating = ''
        else:
            user_rating = ''

        context['user_rating'] = user_rating
        context['tags'] = tags
        context['rating'] = rating
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_rating = data['user_rating']
        response = {'message': ''}
        try:
            feedback = self.request.user.feedback.get(post=self.get_object())

            if user_rating == 'L':
                feedback.feedback = 'L'
            elif user_rating == 'D':
                feedback.feedback = 'D'
            else:
                feedback.delete()

        except:
            feedback = PostFeedBack.objects.create(
                    user=self.request.user,
                    feedback='',
                    post=self.get_object(),
                    )
            if user_rating == 'L':
                feedback.feedback = 'L'
            elif user_rating == 'D':
                feedback.feedback = 'D'
            feedback.save()

        return JsonResponse(response, status=200)


class UserList(ListView):
    template_name = 'main/user-list.html'
    context_object_name = 'users'
    model = user_model


class UserDetail(DetailView):
    template_name = 'main/user-detail.html'
    context_object_name = 'user'
    model = user_model
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object)[:7]
        fields = {}

        for field in self.model_fields:
            value = getattr(self.object, field)
            fields[field] = value

        fields['uploads'] = len(self.object.post_set.all())
        context['fields'] = fields
        context['posts'] = posts

        return context


class TagList(ListView):
    template_name = 'main/tag-list.html'
    context_object_name = 'tags'
    model = Tag


class UpdateTag(UpdateView):
    template_name = 'main/tag-update.html'
    model = Tag
    pk_url_kwarg = 'id'
    fields = ['name',]

    def get_success_url(self):
        return reverse_lazy('tag-update', args=(self.object.id,))


class CreateTag(CreateView):
    template_name = 'main/tag-detail.html'
    context_object_name = 'tag'
    model = Tag
    fields = ['name',]

    def get_success_url(self):
        return reverse_lazy('tag-update', args=(self.object.id,))


class DeleteTag(DeleteView):
    template_name = 'main/tag-delete.html'
    model = Tag
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('tag-list')
