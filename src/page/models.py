from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """
    Model that represents post data
    """

    title = models.CharField(max_length=50)
    content = models.TextField('content')
    date_posted = models.DateTimeField('time published', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('page:detail', args=[self.pk])

    def __str__(self):
        return self.title
