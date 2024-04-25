from django.db import models
from django.conf import settings
user_model = settings.AUTH_USER_MODEL

class Post(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.name


class PostFeedBack(models.Model):
    choices = (
            ('L', 'Like'),
            ('D', 'Dislike'),
            )
    user = models.ForeignKey(user_model, on_delete=models.PROTECT, related_name='feedback')
    feedback = models.CharField(max_length=1, choices=choices)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='feedback')

    def __str__(self):
        return self.feedback


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    post = models.ManyToManyField('Post', related_name='tags')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
