from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from . import serializers
from . import permissions as api_perm
from page.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit posts.
    """

    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_perm.IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        api_perm.IsOwnerOrReadOnly
    ]
