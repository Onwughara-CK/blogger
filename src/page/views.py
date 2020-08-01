from django.shortcuts import render
from django.views import generic

from . import models


class HomeView(generic.ListView):
    model = models.Post
    template_name = "page/home.html"
    ordering = ['-date_posted']
    context_object_name = 'posts'
