from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from . import models


class HomeView(generic.ListView):
    model = models.Post
    template_name = "page/home.html"
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = "page/post_detail.html"
    context_object_name = 'post'


class PostRedirectDetailView(RedirectView):
    permanent = True
    query_string = True
    pattern_name = 'page:home'

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['pk'])
        return post.get_absolute_url()


class PostCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        post = self.get_object()
        if post.author != user:
            raise PermissionDenied
        return handler


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Post
    success_message = 'Successfully deleted Post'
    success_url = reverse_lazy('page:home')

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        post = self.get_object()
        if post.author != user:
            raise PermissionDenied
        return handler


class UserPostListView(generic.ListView):
    """
    RETURNS all post by a particular user
    and also the user object
    """

    template_name = "page/owner_post_list.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username']).first().posts.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_owner'] = User.objects.get(
            username=self.kwargs['username'])
        return context
