from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id', 'title', 'slug','publish', 'body', 'status')

        extra_kwargs={
            'author':{'read_only':True},
            'publish':{'read_only':True}
        }
