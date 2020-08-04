from django.urls import reverse_lazy
from django.views import generic

from . import models


class HomeView(generic.ListView):
    model = models.Post
    template_name = "page/home.html"
    ordering = ['-date_posted']
    context_object_name = 'posts'


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = "page/post_detail.html"
    context_object_name = 'post'


class PostCreateView(generic.edit.CreateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(generic.edit.UpdateView):
    model = models.Post
    fields = ('title', 'content', 'date_posted')


class PostDeleteView(generic.edit.DeleteView):
    model = models.Post
    success_url = reverse_lazy('page:home')
