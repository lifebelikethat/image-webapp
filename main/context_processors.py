from django.contrib.auth.models import User
from .models import Tag
import json

def all_tags(request):
    tags = json.dumps(list(Tag.objects.values_list('name', flat=True)))
    # tags = json.dumps(list(Tag.objects.values()))
    return {
            'all_tags': tags,
            }
