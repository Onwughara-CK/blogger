from page.models import Post

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Post.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'posts']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'content', 'date_posted', 'author']
        read_only_fields = ['date_posted', 'author']
