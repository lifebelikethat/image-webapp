from django import forms
from .models import Post, Tag


class PostEditForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            required=False,
            )

    class Meta:
        model = Post
        fields = ('name', 'description', 'tags',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].initial = self.instance.tags.all().values_list('id', flat=True)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        instance.tags.set(self.cleaned_data['tags'])
        return instance


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'description', 'image',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs, commit=False)
        instance.author = self.user
        instance.save()
        return instance
