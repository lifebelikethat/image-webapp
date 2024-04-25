from django.contrib import admin
from .models import Post, PostFeedBack, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(PostFeedBack)
admin.site.register(Tag)

