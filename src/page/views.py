from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')
    success_message = 'Successfully created Post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')
    success_message = 'Successfully Updated Post'

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        if post.author != user:
            raise PermissionDenied
        return True


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.edit.DeleteView):
    model = models.Post
    success_url = reverse_lazy('page:home')
    success_message = 'Successfully Updated Post'

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        if post.author != user:
            raise PermissionDenied
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


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


class ApiDocs(TemplateView):
    template_name = "page/api.html"
